import unittest
import plugins.nmap_scanner  # noqa: F401
import plugins.traffic_capture  # noqa: F401
import plugins.password_guess  # noqa: F401
from app.core import registry

class TestPlugins(unittest.TestCase):
    def test_nmap_validate(self):
        p = registry.get("nmap_scanner")
        self.assertIsNotNone(p.validate({}))  # нет target
        self.assertIsNone(p.validate({"target": "127.0.0.1"}))
        self.assertIsNone(p.validate({"target": "192.168.1.0/24"}))
        self.assertIsNotNone(p.validate({"target": "bad_target"}))

    def test_nmap_build(self):
        p = registry.get("nmap_scanner")
        cmd = p.build_command({"target": "127.0.0.1", "flags": "-sV"})
        self.assertEqual(cmd[:2], ["nmap", "-sV"])

    def test_capture_validate(self):
        p = registry.get("traffic_capture")
        self.assertIsNotNone(p.validate({}))
        self.assertIsNone(p.validate({"iface": "eth0"}))
        self.assertIsNotNone(p.validate({"iface": "eth0", "filter": "port 99999"}))

    def test_password_guess_validate(self):
        p = registry.get("password_guess")
        self.assertIsNotNone(p.validate({}))
        ok = {"service": "ssh", "target": "127.0.0.1", "user": "root", "wordlist": "/usr/share/wordlists/rockyou.txt"}
        self.assertIsNone(p.validate(ok))

if __name__ == "__main__":
    unittest.main()
