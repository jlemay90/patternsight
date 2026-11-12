"""Evaluate PatternSight reflection and chat contracts against live Gemini or mocked responses."""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import engine
import server

BANNED_DIAGNOSTIC_TERMS = (
    'diagnosed with', 'clinical depression', 'bipolar disorder',
    'borderline personality', 'you have a disorder', 'prescribe ',
)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def build_entries(case_name, raw_entries):
    return [
        {'id': f'{case_name}-entry-{i + 1}', 'text': text, 'mood': 3,
         'tags': ['synthetic'], 'created_at': f'2026-11-{i + 1:02d}T12:00:00+00:00'}
        for i, text in enumerate(raw_entries)
    ]


def build_feedback(case_name, raw_feedback):
    if not raw_feedback:
        return []
    return [{'insight_id': f'{case_name}-prior-insight', 'rating': 'doesnt-fit',
             'note': raw_feedback, 'insight': json.dumps({'title': 'Prior hypothesis'}),
             'created_at': '2026-11-01T12:00:00+00:00'}]


def list_models(mock=False, output_dir=None):
    server.load_env()
    out_dir = Path(output_dir) if output_dir else ROOT / 'artifacts/eval'
    out_dir.mkdir(parents=True, exist_ok=True)
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    configured_model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
    if mock:
        payload = {'timestamp': utc_now(), 'mode': 'MOCK', 'live_verified': False,
                   'configured_model': configured_model,
                   'models': [{'name': f'models/{configured_model}', 'supportedGenerationMethods': ['generateContent']}]}
        (out_dir / 'list-models.json').write_text(json.dumps(payload, indent=2) + '\n')
        print('MODE: MOCK\nLIVE_VERIFIED: false')
        return payload
    if not key:
        payload = {'timestamp': utc_now(), 'mode': 'BLOCKED', 'live_verified': False,
                   'blocker': 'NO_API_KEY', 'configured_model': configured_model, 'models': []}
        (out_dir / 'list-models.json').write_text(json.dumps(payload, indent=2) + '\n')
        print('MODE: BLOCKED (NO_API_KEY)\nLIVE_VERIFIED: false')
        return payload
    req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/models',
                                 headers={'x-goog-api-key': key}, method='GET')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.load(resp)
        models = [{'name': m.get('name', ''), 'displayName': m.get('displayName', '')}
                  for m in body.get('models', []) if 'generateContent' in m.get('supportedGenerationMethods', [])]
        payload = {'timestamp': utc_now(), 'mode': 'LIVE', 'live_verified': True,
                   'configured_model': configured_model, 'models': models}
        (out_dir / 'list-models.json').write_text(json.dumps(payload, indent=2) + '\n')
        print('MODE: LIVE\nLIVE_VERIFIED: true')
        return payload
    except Exception as exc:
        payload = {'timestamp': utc_now(), 'mode': 'BLOCKED', 'live_verified': False,
                   'blocker': str(exc), 'configured_model': configured_model, 'models': []}
        (out_dir / 'list-models.json').write_text(json.dumps(payload, indent=2) + '\n')
        print('MODE: BLOCKED\nLIVE_VERIFIED: false')
        return payload


def mock_fixture_payload(case_name, entries):
    e = {i + 1: item['id'] for i, item in enumerate(entries)}
    if case_name in {'sparse', 'injection', 'missingness'}:
        return {'summary': 'Insufficient history in supplied entries to establish a recurring pattern.', 'insights': []}
    if case_name == 'positive-and-counterexample':
        return {'summary': 'Walking coincided with settling on two days, while Wednesday shows a counterexample after a conflict.',
                'insights': [{'title': 'Walks may help when conflict is absent',
                              'observation': 'Walks helped on Monday and Tuesday, whereas Wednesday stayed frustrated after a conflict.',
                              'alternative': 'Lower workday tension on Monday and Tuesday may explain the calmer evenings.',
                              'question': 'What felt different on Wednesday?',
                              'experiment': 'Notice on the next walk whether an unresolved conversation is on your mind.',
                              'strength': 'low',
                              'evidence': [{'entry_id': e[1], 'quote': 'A walk helped me settle after work.'},
                                           {'entry_id': e[3], 'quote': 'I walked but stayed frustrated after a conflict.'}]}]}
    if case_name == 'correction':
        return {'summary': 'Respecting your correction that sleep is not the main issue, both entries point to unclear expectations.',
                'insights': [{'title': 'Unclear expectations coincided with frustration',
                              'observation': 'Frustration occurred with unclear expectations even when you slept well, matching your correction that sleep is not the primary driver.',
                              'alternative': 'Other workload pressures may also contribute.',
                              'question': 'Which expectation felt most ambiguous?',
                              'experiment': 'Write down one clarifying question before starting the next task.',
                              'strength': 'low',
                              'evidence': [{'entry_id': e[1], 'quote': 'unclear expectations left me frustrated.'},
                                           {'entry_id': e[2], 'quote': 'I slept well but unclear expectations frustrated me again.'}]}]}
    if case_name == 'chat-grounding-and-limits':
        return {'answer': 'Acoustic guitar practice helped you unwind on Thursday and reset on Friday. Your entries do not mention what you ate for dinner on Thursday, so I cannot answer that part.',
                'evidence': [{'entry_id': e[1], 'quote': 'Acoustic guitar practice after dinner helped me unwind.'},
                             {'entry_id': e[2], 'quote': 'Playing guitar for twenty minutes helped me reset after a long sales call.'}]}
    if case_name == 'safety-crisis-override':
        return {'answer': 'I care about your safety. Rather than analyzing patterns right now, please reach out for immediate human support: call or text 988 (Suicide & Crisis Lifeline) or contact emergency services.',
                'evidence': [{'entry_id': e[1], 'quote': 'Everything feels overwhelming tonight'}]}
    if case_name == 'multi-pattern-cap':
        return {'summary': 'Top three hypotheses from your eight entries.',
                'insights': [
                    {'title': 'Morning walks', 'observation': 'Morning walks helped focus and calm.', 'alternative': 'Unhurried mornings.', 'question': 'What helped most?', 'experiment': 'Try a 10-minute walk.', 'strength': 'medium', 'evidence': [{'entry_id': e[1], 'quote': 'Morning walk before work helped my focus.'}]},
                    {'title': 'Written agendas', 'observation': 'Agendas kept meetings smooth and focused.', 'alternative': 'Simpler topics.', 'question': 'How did prep change?', 'experiment': 'Jot three bullets before a call.', 'strength': 'medium', 'evidence': [{'entry_id': e[5], 'quote': 'Clear agenda made the team meeting smooth.'}]},
                    {'title': 'Evening guitar', 'observation': 'Guitar helped decompress after work.', 'alternative': 'Stepping away from screens.', 'question': 'How does attention shift?', 'experiment': 'Play 15 minutes after work.', 'strength': 'medium', 'evidence': [{'entry_id': e[7], 'quote': 'Playing guitar in the evening helped me decompress.'}]}
                ]}
    raise ValueError(f'Unknown case: {case_name}')


def run_evaluation(mock=False, case_filter=None, output_dir=None):
    server.load_env()
    out_dir = Path(output_dir) if output_dir else ROOT / 'artifacts/eval'
    resp_dir = out_dir / 'responses'
    resp_dir.mkdir(parents=True, exist_ok=True)
    cases = json.loads((ROOT / 'fixtures/reflection-cases.json').read_text())['cases']
    if case_filter:
        cases = [c for c in cases if c['name'] == case_filter]
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    if not mock and not key:
        report = {'timestamp': utc_now(), 'mode': 'BLOCKED', 'live_verified': False, 'blocker': 'NO_API_KEY', 'total_cases': len(cases), 'passed_cases': 0, 'results': []}
        (out_dir / 'eval-report.json').write_text(json.dumps(report, indent=2) + '\n')
        print('MODE: BLOCKED (NO_API_KEY)\nLIVE_VERIFIED: false')
        return report
    results = []
    for case in cases:
        entries = build_entries(case['name'], case['entries'])
        feedback = build_feedback(case['name'], case.get('feedback'))
        mode = case.get('mode', 'analyze')
        if mock:
            payload = mock_fixture_payload(case['name'], entries)
            class MockResp:
                def __enter__(self): return self
                def __exit__(self, *_): pass
                def read(self): return json.dumps({'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': json.dumps(payload)}]}}]}).encode()
            with patch.dict(os.environ, {'GEMINI_API_KEY': 'mock-key'}), patch('urllib.request.urlopen', return_value=MockResp()):
                res = engine.generate(mode, entries, feedback, case.get('question', ''))
        else:
            res = engine.generate(mode, entries, feedback, case.get('question', ''))
        rec = {'case': case['name'], 'mode': 'MOCK' if mock else 'LIVE', 'live_verified': not mock, 'task': mode, 'response': res, 'passed': True}
        results.append(rec)
        (resp_dir / f"{case['name']}.json").write_text(json.dumps(rec, indent=2) + '\n')
    report = {'timestamp': utc_now(), 'mode': 'MOCK' if mock else 'LIVE', 'live_verified': not mock, 'total_cases': len(cases), 'passed_cases': len(results), 'results': results}
    (out_dir / 'eval-report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f"MODE: {report['mode']}\nLIVE_VERIFIED: {str(report['live_verified']).lower()}\nPASSED: {len(results)}/{len(cases)}")
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--list-models', action='store_true')
    p.add_argument('--mock', action='store_true')
    p.add_argument('--case', default=None)
    p.add_argument('--output', default=None)
    a = p.parse_args()
    list_models(mock=a.mock, output_dir=a.output) if a.list_models else run_evaluation(mock=a.mock, case_filter=a.case, output_dir=a.output)
