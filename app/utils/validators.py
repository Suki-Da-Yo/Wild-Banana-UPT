# Здесь будут общие функции проверки (IP, порты и т.д.)
import ipaddress

def is_valid_ip(ip: str) -> bool:
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_cidr(net: str) -> bool:
    try:
        ipaddress.ip_network(net, strict=False)
        return True
    except ValueError:
        return False

def is_valid_port(port) -> bool:
    try:
        p = int(port)
        return 1 <= p <= 65535
    except Exception:
        return False
