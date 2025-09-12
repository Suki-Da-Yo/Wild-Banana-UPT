import re, yaml
from pathlib import Path
from typing import Dict, Any

_rules = yaml.safe_load(Path(__file__).with_name("rules.yaml").read_text())

def infer_intent(text: str) -> Dict[str, Any]:
    for rule in _rules["intents"]:
        if re.search(rule["pattern"], text, flags=re.IGNORECASE):
            action = rule["action"]
            params = dict(_rules["defaults"].get(action, {}).get("params", {}))
            return {"action": action, "params": params}
    return {"action": None, "params": {}}
