##
## EPITECH PROJECT, 2026
## Dashboard
## File description:
## registry.py
##

from typing import Callable, List, Dict, Any

WIDGET_REGISTRY = {}

def register_widget(service: str, name: str, type: str, description: str, params: List[Dict[str, Any]]):
    def decorator(func: Callable):
        WIDGET_REGISTRY[type] = {
            "service": service,
            "name": name,
            "type": type,
            "description": description,
            "params": params,
            "handler": func
        }
        return func
    return decorator