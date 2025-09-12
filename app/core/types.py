from typing import Dict, Any, Optional, List, Protocol

class Plugin(Protocol):
    name: str
    capabilities: List[str]
    def validate(self, params: Dict[str, Any]) -> Optional[str]: ...
    def build_command(self, params: Dict[str, Any]) -> List[str]: ...
