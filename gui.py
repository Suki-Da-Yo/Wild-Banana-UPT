# gui.py — минимальный GUI на Tkinter для v0.1
import json
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from app.core import registry
from app.core.executor import run_command, SafetyError
from app.core.config import settings
from app.ai.intent import infer_intent

# Импортируем плагины, чтобы они зарегистрировались
import plugins.nmap_scanner  # noqa: F401
import plugins.traffic_capture  # noqa: F401
import plugins.password_guess  # noqa: F401


class UnifiedPentestGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Unified Pentest (v0.1-alpha)")
        self.geometry("800x600")

        # Заголовок
        title = ttk.Label(self, text="Unified Pentest (v0.1-alpha)", font=("Helvetica", 16))
        title.pack(pady=8)

        # Поле ввода
        self.input_box = ScrolledText(self, height=4)
        self.input_box.pack(fill="x", padx=10)

        # Кнопки
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=6)

        self.chat_btn = ttk.Button(btn_frame, text="Chat", command=self.on_chat)
        self.chat_btn.grid(row=0, column=0, padx=5)

        self.run_btn = ttk.Button(btn_frame, text="Run", command=self.on_run)
        self.run_btn.grid(row=0, column=1, padx=5)

        self.legal_btn = ttk.Button(btn_frame, text="Legal ON/OFF", command=self.on_toggle_legal)
        self.legal_btn.grid(row=0, column=2, padx=5)

        self.exit_btn = ttk.Button(btn_frame, text="Exit", command=self.destroy)
        self.exit_btn.grid(row=0, column=3, padx=5)

        # Вывод
        self.output_box = ScrolledText(self, height=20, state="disabled")
        self.output_box.pack(fill="both", expand=True, padx=10, pady=6)

        self.log(f"Legal mode = {settings.legal_mode}, dry_run = {settings.dry_run}")

    def get_input(self) -> str:
        return self.input_box.get("1.0", "end").strip()

    def log(self, text: str):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def on_toggle_legal(self):
        settings.legal_mode = not settings.legal_mode
        self.log(f"Legal mode = {settings.legal_mode}")

    def on_chat(self):
        q = self.get_input()
        if not q:
            self.log("Введите запрос, например: «скан 192.168.1.0/24».")
            return

        hint = infer_intent(q)
        if not hint["action"]:
            self.log("Не понял запрос.")
            return

        plugin = next((p for p in registry.all_plugins() if hint["action"] in p.capabilities), None)
        if not plugin:
            self.log("Нет подходящего плагина.")
            return

        err = plugin.validate(hint["params"])
        if err:
            self.log("Нужно уточнить параметры: " + err)
            return

        cmd = plugin.build_command(hint["params"])
        self.log("Предлагаемая команда: " + " ".join(cmd))
        self.log(f"Для запуска из CLI: python cli.py run {plugin.name} --params '{json.dumps(hint['params'])}'")

    def on_run(self):
        # В поле ввода ожидаем ИМЯ плагина (например: nmap_scanner)
        q = self.get_input()
        if not q:
            self.log("Укажите имя плагина (например, nmap_scanner).")
            return

        try:
            plugin = registry.get(q)
        except KeyError:
            self.log(f"Нет плагина с именем: {q}")
            return

        # Пытаемся собрать команду с пустыми параметрами — если нужно, плагин попросит доп. поля
        err = plugin.validate({})
        if err:
            self.log("Нужно уточнить параметры: " + err)
            return

        cmd = plugin.build_command({})
        try:
            out = run_command(cmd)
            self.log(out)
        except SafetyError as e:
            self.log("[Безопасность] " + str(e))


if __name__ == "__main__":
    app = UnifiedPentestGUI()
    app.mainloop()