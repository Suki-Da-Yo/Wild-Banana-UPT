import json
import os

CONFIG_FILE = "settings.json"

class Settings:
    def __init__(self):
        # значения по умолчанию
        self.legal_mode: bool = False
        self.dry_run: bool = True
        self.sudo: bool = False
        # пробуем загрузить сохранённые
        self.load()

    def save(self) -> None:
        data = {
            "legal_mode": self.legal_mode,
            "dry_run": self.dry_run,
            "sudo": self.sudo,
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(data, f)

    def load(self) -> None:
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r") as f:
                    data = json.load(f)
                self.legal_mode = bool(data.get("legal_mode", False))
                self.dry_run = bool(data.get("dry_run", True))
                self.sudo = bool(data.get("sudo", False))
            except Exception:
                # если файл битый — игнорируем и оставляем дефолты
                pass

settings = Settings()
