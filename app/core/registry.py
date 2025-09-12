from typing import Dict
from app.core.types import Plugin

_registry: Dict[str, Plugin] = {}

def register(plugin: Plugin):
    _registry[plugin.name] = plugin

def get(name: str) -> Plugin:
    return _registry[name]

def all_plugins():
    return list(_registry.values())
