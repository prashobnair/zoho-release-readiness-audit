"""Offline config-manifest diff; not a Zoho metadata parser or deployer."""
from __future__ import annotations
import hashlib
import json

KINDS = {'field', 'layout', 'workflow', 'validation', 'function', 'webhook'}
SENSITIVE = {'workflow', 'validation', 'function', 'webhook'}


def index(items):
    if not isinstance(items, list):
        raise ValueError('components must be list')
    result = {}
    for item in items:
        if not isinstance(item, dict) or item.get('kind') not in KINDS or not isinstance(item.get('name'), str) or not item['name']:
            raise ValueError('Invalid component')
        key = (item['kind'], item['name'])
        if key in result:
            raise ValueError('Duplicate component')
        deps = item.get('depends_on', [])
        if not isinstance(deps, list) or any(not isinstance(d, str) for d in deps):
            raise ValueError('depends_on must be a string list')
        result[key] = item
    return result


def compare(before, after):
    old = index(before)
    new = index(after)
    findings = []
    changes = []
    keys = sorted(old.keys() | new.keys())
    for kind, name in keys:
        key = (kind, name)
        prior, later = old.get(key), new.get(key)
        if prior is None:
            change = 'added'
        elif later is None:
            change = 'removed'
        elif prior != later:
            change = 'changed'
        else:
            continue
        changes.append({'kind':kind,'name':name,'change':change})
        if kind in SENSITIVE:
            findings.append({'code':'behavior_regression_review','component':f'{kind}:{name}'})
        if change == 'removed':
            findings.append({'code':'removal_review','component':f'{kind}:{name}'})
    existing = {f'{kind}:{name}' for kind, name in new}
    for (kind, name), item in sorted(new.items()):
        for dep in item.get('depends_on', []):
            if dep not in existing:
                findings.append({'code':'missing_dependency','component':f'{kind}:{name}','dependency':dep})
    findings.sort(key=lambda x:(x['code'], x['component'], x.get('dependency','')))
    fingerprint = hashlib.sha256(json.dumps(after, sort_keys=True, separators=(',',':')).encode()).hexdigest()
    return {'mode':'dry_run_only','ready_for_release':not findings,'changes':changes,'findings':findings,
            'target_manifest_sha256':fingerprint,'deployment_actions':0}
