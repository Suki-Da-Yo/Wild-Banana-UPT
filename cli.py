import typer
import json
from app.core import registry
from app.core.executor import run_command, SafetyError
from app.core.config import settings
from app.ai.intent import infer_intent

# импортируем плагины, чтобы они зарегистрировались в реестре
import plugins.nmap_scanner  # noqa: F401
import plugins.traffic_capture  # noqa: F401
import plugins.password_guess  # noqa: F401

app = typer.Typer(help="Unified Pentest (v0.1-alpha)")

@app.command()
def legal(
    agree: bool = typer.Option(False, help="Подтверждаю авторизованное тестирование"),
    dry_run: bool = typer.Option(True, help="Показывать команды, не запускать"),
):
    settings.legal_mode = agree
    settings.dry_run = dry_run
    settings.save()  # <-- Сохраняем на диск, чтобы не сбрасывалось между запусками
    typer.echo(f"legal_mode={settings.legal_mode}, dry_run={settings.dry_run}")

@app.command()
def run(plugin: str, params: str = typer.Option("{}", help='JSON вида {"target":"..."}')):
    p = json.loads(params)
    p_obj = registry.get(plugin)
    err = p_obj.validate(p)
    if err:
        raise typer.BadParameter(err)
    cmd = p_obj.build_command(p)
    try:
        out = run_command(cmd)
        typer.echo(out)
    except SafetyError as e:
        typer.echo(f"[Безопасность] {e}")

@app.command()
def chat(q: str):
    hint = infer_intent(q)
    if not hint["action"]:
        return typer.echo("Не понял запрос. Примеры: 'скан 192.168.1.0/24'")
    plugin = next((p for p in registry.all_plugins() if hint["action"] in p.capabilities), None)
    if not plugin:
        return typer.echo("Нет подходящего плагина.")
    err = plugin.validate(hint["params"])
    if err:
        return typer.echo(f"Нужно уточнить параметры: {err}")
    cmd = plugin.build_command(hint["params"])
    typer.echo("Предлагаемая команда: " + " ".join(cmd))
    typer.echo(f"Запуск: python cli.py run {plugin.name} --params '{json.dumps(hint['params'])}'")

if __name__ == "__main__":
    app()
