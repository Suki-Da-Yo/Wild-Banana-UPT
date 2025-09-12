import unittest
from app.utils.validators import is_valid_ip, is_valid_cidr, is_valid_port

class TestValidators(unittest.TestCase):
    def test_ip(self):
        self.assertTrue(is_valid_ip("127.0.0.1"))
        self.assertFalse(is_valid_ip("999.0.0.1"))

    def test_cidr(self):
        self.assertTrue(is_valid_cidr("192.168.1.0/24"))
        self.assertFalse(is_valid_cidr("192.168.1.0/99"))

    def test_port(self):
        self.assertTrue(is_valid_port(22))
        self.assertFalse(is_valid_port(70000))

if __name__ == "__main__":
    unittest.main()
