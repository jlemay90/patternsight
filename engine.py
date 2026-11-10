"""Versioned Gemini contract and deterministic, testable evidence validation."""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent
PROMPT_VERSION = 'reflect-v1'
EVIDENCE = {'type': 'OBJECT', 'properties': {
    'entry_id': {'type': 'STRING'}, 'quote': {'type': 'STRING'}},
    'required': ['entry_id', 'quote']}
INSIGHT = {'type': 'OBJECT', 'properties': {
    **{k: {'type': 'STRING'} for k in ['title', 'observation', 'alternative', 'question', 'experiment']},
    'strength': {'type': 'STRING', 'enum': ['low', 'medium']},
    'evidence': {'type': 'ARRAY', 'items': EVIDENCE}},
    'required': ['title', 'observation', 'alternative', 'question', 'experiment', 'strength', 'evidence']}
SCHEMAS = {
    'analyze': {'type': 'OBJECT', 'properties': {
        'summary': {'type': 'STRING'}, 'insights': {'type': 'ARRAY', 'items': INSIGHT, 'maxItems': 3}},
        'required': ['summary', 'insights']},
    'chat': {'type': 'OBJECT', 'properties': {
        'answer': {'type': 'STRING'}, 'evidence': {'type': 'ARRAY', 'items': EVIDENCE}},
        'required': ['answer', 'evidence']}}


class ProviderError(Exception):
    pass


def check_text(obj, key, maximum=8000):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > maximum:
        raise ValueError(f'Invalid {key}')


def validate_evidence(evidence, entries, required=False):
    if not isinstance(evidence, list) or len(evidence) > 30 or (required and not evidence):
        raise ValueError('Invalid evidence list')
    lookup = {e['id']: e['text'] for e in entries}
    for item in evidence:
        if not isinstance(item, dict):
            raise ValueError('Invalid evidence')
        if not isinstance(item.get('entry_id'), str) or item['entry_id'] not in lookup:
            raise ValueError('Unknown evidence entry')
        quote = item.get('quote')
        if not isinstance(quote, str) or not quote.strip() or quote not in lookup[item['entry_id']]:
            raise ValueError('Evidence quote does not match source')


def validate_result(result, mode, entries):
    if not isinstance(result, dict):
        raise ValueError('Expected an object')
    if mode == 'chat':
        check_text(result, 'answer')
        validate_evidence(result.get('evidence'), entries)
    else:
        check_text(result, 'summary')
        insights = result.get('insights')
        if not isinstance(insights, list) or len(insights) > 3:
            raise ValueError('Expected zero to three insights')
        for item in insights:
            if not isinstance(item, dict):
                raise ValueError('Invalid insight')
            for key in ['title', 'observation', 'alternative', 'question', 'experiment']:
                check_text(item, key, 3000)
            if item.get('strength') not in ('low', 'medium'):
                raise ValueError('Invalid strength')
            validate_evidence(item.get('evidence'), entries, required=True)
    return result


def generate(mode, entries, feedback, question=''):
    key = os.environ.get('GEMINI_API_KEY', '').strip()
    model = os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
    if not key:
        raise ProviderError('AI is not connected. Set GEMINI_API_KEY in .env and restart the server.')
    if not re.fullmatch(r'[a-zA-Z0-9_.-]+', model):
        raise ProviderError('Invalid GEMINI_MODEL configuration.')
    context = {'task': mode, 'entries': entries, 'owner_feedback': feedback, 'question': question}
    payload = {
        'systemInstruction': {'parts': [{'text': (ROOT / 'prompts/reflect-v1.txt').read_text()}]},
        'contents': [{'role': 'user', 'parts': [{'text': json.dumps(context)}]}],
        'generationConfig': {'temperature': 0.2, 'maxOutputTokens': 8192,
                             'responseMimeType': 'application/json', 'responseSchema': SCHEMAS[mode]}}
    request = urllib.request.Request(
        f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
        data=json.dumps(payload).encode(),
        headers={'Content-Type': 'application/json', 'x-goog-api-key': key}, method='POST')
    try:
        with urllib.request.urlopen(request, timeout=55) as response:
            body = json.load(response)
        candidate = body['candidates'][0]
        if candidate.get('finishReason') != 'STOP':
            raise ProviderError('The model did not finish its response. Try a smaller context or another model.')
        raw = ''.join(p.get('text', '') for p in candidate['content']['parts'] if not p.get('thought'))
        return validate_result(json.loads(raw), mode, entries)
    except urllib.error.HTTPError as exc:
        # Never return provider bodies: they may echo private text or credentials.
        raise ProviderError(f'Google returned HTTP {exc.code}. Check the model, API key and quota; your entries remain saved.') from None
    except (urllib.error.URLError, TimeoutError):
        raise ProviderError('Google could not be reached. Your entries remain saved; try again later.') from None
    except (KeyError, IndexError, TypeError, ValueError):
        raise ProviderError('The model response failed structure or exact-quote checks. No new analysis was saved.') from None
