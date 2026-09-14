import json
from pathlib import Path

def test_actor_json_exists_and_valid():
    actor_file = Path(".actor/actor.json")
    assert actor_file.exists(), ".actor/actor.json must exist"
    data = json.loads(actor_file.read_text(encoding="utf-8"))
    assert data["actorSpecification"] == 1
    assert data["name"] == "yc-talent-radar"
    assert "dockerfile" in data

def test_input_schema_valid():
    schema_file = Path(".actor/input_schema.json")
    assert schema_file.exists(), ".actor/input_schema.json must exist"
    schema = json.loads(schema_file.read_text(encoding="utf-8"))
    assert schema["schemaVersion"] == 1
    props = schema["properties"]
    assert "searchQuery" in props
    assert "roles" in props
    assert "maxItems" in props
