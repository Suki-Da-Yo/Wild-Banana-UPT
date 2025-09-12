from app.utils.validators import is_valid_ip, is_valid_cidr
from typing import Dict, Any, List, Optional
from app.core import registry


class NmapScanner:
    name = "nmap_scanner"
    capabilities = ["nmap_scan"]

    def validate(self, params):
        tgt = params.get("target")
        if not tgt:
            return "Укажите target (IP или подсеть CIDR, напр. 192.168.1.0/24)"
        if not (is_valid_ip(tgt) or is_valid_cidr(tgt)):
            return "Некорректный target: ожидается IP или CIDR"
        return None


    def build_command(self, params: Dict[str, Any]) -> List[str]:
        flags = params.get("flags", "-sV")
        target = params["target"]
        return ["nmap", *flags.split(), target]

registry.register(NmapScanner())