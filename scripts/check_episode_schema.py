"""Structural-only M0 schema checks. Fixtures are entirely fictional."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

root = Path(__file__).resolve().parents[1]
schema = json.loads((root / 'schemas/problem-episode.schema.json').read_text())
Draft202012Validator.check_schema(schema)
validator = Draft202012Validator(schema)
fixtures = sorted((root / 'fixtures/episode-schema').glob('*.json'))
assert len(fixtures) == 3, 'expected three fictional fixtures'
for path in fixtures:
    instance = json.loads(path.read_text())
    validator.validate(instance)
    print('PASS', path.name)
base = json.loads(fixtures[0].read_text())
missing = copy.deepcopy(base)
missing.pop('uncertainty')
invalid_actor = copy.deepcopy(base)
invalid_actor['problem_formulations'][0]['type'] = 'reconstructed_actor'
invalid_edge = copy.deepcopy(base)
invalid_edge['relations'] = [{'to_episode':'other','relation':'continuous','status':'supported','continuity_evidence':[]}]
for name, sample in [('missing uncertainty',missing),('actor gate',invalid_actor),('relation gate',invalid_edge)]:
    assert not validator.is_valid(sample), f'FAIL: accepted {name}'
    print('REJECTED',name)
print('Structural checks passed; historical claims NOT validated')
