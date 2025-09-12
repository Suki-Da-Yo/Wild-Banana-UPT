from app.utils.validators import is_valid_port  # пригодится, если введут порт в фильтре
from typing import Dict, Any, List, Optional
from app.core import registry

class TrafficCapture:
    name = "traffic_capture"
    capabilities = ["traffic_capture"]

    def validate(self, params):
        if "iface" not in params:
            return "Укажите iface (например, eth0)"
        # Простейшая подсказка: если передали filter вида 'port X' — проверим X
        flt = params.get("filter")
        if flt and flt.strip().startswith("port "):
            maybe_port = flt.strip().split()[-1]
            if not is_valid_port(maybe_port):
                return "Некорректный номер порта в фильтре"
        return None

    def build_command(self, params: Dict[str, Any]) -> List[str]:
        iface = params["iface"]
        bpf = params.get("filter")
        outfile = params.get("outfile", "capture.pcap")
        cmd = ["tcpdump", "-i", iface, "-w", outfile]
        if bpf:
            cmd += [bpf]
        return cmd

registry.register(TrafficCapture())
