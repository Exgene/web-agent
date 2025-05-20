import inspect
from typing import Type


def generate_json_from_tool_calls(cls: Type) -> list[dict[str, any]]:
    functions: list[dict] = []
    for name, func in inspect.getmembers(cls, inspect.isfunction):
        if name.startswith("__") and name.endswith("__"):
            continue
        sig = inspect.signature(func)
        params = {"type": "object", "properties": {}, "required": []}
        for param_name, param in sig.parameters.items():
            if param_name == "self":
                continue
            param_type = (
                str(param.annotation)
                if param.annotation != inspect._empty
                else "string"
            )
            params["properties"][param_name] = {"type": param_type}
            if param.default == inspect._empty:
                params["required"].append(param_name)
        functions.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": func.__doc__ or "",
                    "parameters": params,
                },
            }
        )
    return functions
