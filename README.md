# Unified Pentest (v0.1-alpha)

Модульный инструмент для пентест-лаборатории с **CLI**, минимальным **GUI** и простым rule-based «ИИ-подсказчиком».  
> ⚠️ Используйте **только** в рамках авторизованного тестирования. По умолчанию включён `dry_run`.

## Возможности v0.1
- **CLI (Typer):** команды `legal`, `run`, `chat`
- **GUI (Tkinter):** окно с полем ввода, кнопками **Chat / Run / Legal / Exit**, область вывода
- **Плагины v0.1:** `nmap_scanner`, `traffic_capture`, `password_guess`
- **ИИ-подсказчик (rule-based):** распознаёт простые запросы и предлагает команды
- **Безопасность:** `legal_mode` и `dry_run` (по умолчанию включен `dry_run`)
- **Тесты:** `unittest` на валидаторы и плагины

## Установка
```bash
git clone https://github.com/<YOUR_GH_USERNAME>/unified-pentest.git](https://github.com/Suki-Da-Yo/unified-pentest.git
cd unified-pentest
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

## Быстрый старт (CLI)
python cli.py legal --agree --dry-run
python cli.py chat "скан 192.168.1.0/24"
python cli.py run nmap_scanner --params '{"target":"127.0.0.1"}'

## Быстрый старт (GUI)
python3 gui.py

В окне:
Chat → введите «скан 192.168.1.0/24»
Legal ON/OFF → переключает legal_mode
Run → введите имя плагина (например nmap_scanner)

## Структура проекта
unified-pentest/
  app/
    core/        # settings, executor, registry
    ai/          # rules.yaml, intent.py
    utils/       # validators.py
  plugins/       # nmap_scanner.py, traffic_capture.py, password_guess.py
  tests/         # unit-тесты
  cli.py         # CLI (Typer)
  gui.py         # GUI (Tkinter)

## Тесты
python -m unittest discover -s tests -v

## Лицензия
Проект распространяется по лицензии MIT (см. LICENSE).
