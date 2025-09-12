import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
import subprocess
from typing import List
from app.core.config import settings

class SafetyError(Exception):
    pass

def run_command(cmd: List[str]) -> str:
    if not settings.legal_mode:
        raise SafetyError("Legal mode выключен.")

    # <--- Логируем всегда перед запуском
    logging.info("Command: %s", " ".join(cmd))

    if settings.dry_run:
        return "[DRY-RUN] " + " ".join(cmd)

    try:
        out = subprocess.run(cmd, capture_output=True, text=True)
        return out.stdout or out.stderr or "Команда выполнена без вывода."
    except subprocess.CalledProcessError as e:
        return (e.stdout or "") + (e.stderr or "")