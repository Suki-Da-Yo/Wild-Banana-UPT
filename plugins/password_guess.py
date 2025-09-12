from app.utils.validators import is_valid_ip
from typing import Dict, Any, List, Optional
from app.core import registry

class PasswordGuess:
    name = "password_guess"
    capabilities = ["password_guess"]

    def validate(self, params):
        required = ["service", "target", "user", "wordlist"]
        missing = [k for k in required if k not in params]
        if missing:
            return f"Недостающие параметры: {', '.join(missing)}"
        if not (is_valid_ip(params["target"]) or params["target"]):  # допускаем домен
            pass  # домены пока не валидируем
        return None

    def build_command(self, params: Dict[str, Any]) -> List[str]:
        return ["hydra", "-l", params["user"], "-P", params["wordlist"], f'{params["service"]}://{params["target"]}']

registry.register(PasswordGuess())
