"""
Autopsy script reconstructed from the class transcript, with the schema adapters
filled in for data/novatech/m1/autopsy_window.json.

Run from the work folder: uv run python labs/m1/autopsy_class.py
"""

import json
from pathlib import Path

BUDGET = 12_000

JSON_PATH = Path("data/novatech/m1/autopsy_window.json")


def get_components(window):
    """Return the context window's components in their stored order."""
    return window["components"]


def get_parts(component):
    """Return the parts belonging to one component.

    This JSON has no nested parts: each component holds its own text.
    """
    return [component]


def get_part_role_and_text(part):
    """Return (role, text) for one part, or (None, None) if not applicable."""
    roles = {"user_input": "user", "system": "system"}
    role = roles.get(part["component"])
    if role is None:
        return None, None
    return role, part["content"]


def get_component_name(component):
    """Return a display name for a component."""
    return component["component"]


def get_component_tokens(component):
    """Return this component's token count as a number."""
    return component["tokens"]


def get_total_window_tokens(window, component_token_counts):
    """Return the window's total token count as a number."""
    return window.get("total_window_tokens", sum(component_token_counts))


def main():
    if not JSON_PATH.is_file():
        raise FileNotFoundError(
            f"Context-window JSON file not found (run from the work folder): {JSON_PATH}"
        )

    window = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    components = list(get_components(window))
    component_token_counts = []

    print("USER QUESTION AND ASSISTANT ANSWER")
    print(f"ASKED BY: {window['persona']}")
    for component in components:
        for part in get_parts(component):
            role, text = get_part_role_and_text(part)
            if role == "user":
                print(f"{role.upper()}: {text}")
    # The answer is a top-level field, not one of the components.
    print(f"ASSISTANT: {window['response']}")

    print("\nTOKENS BY COMPONENT")
    for component in components:
        component_name = get_component_name(component)
        tokens = get_component_tokens(component)
        component_token_counts.append(tokens)
        percent_of_budget = (tokens / BUDGET) * 100
        print(
            f"{component_name}: {tokens:,} tokens "
            f"({percent_of_budget:.2f}% of {BUDGET:,})"
        )

    total_tokens = get_total_window_tokens(window, component_token_counts)
    total_percent = (total_tokens / BUDGET) * 100
    print(
        f"TOTAL WINDOW: {total_tokens:,} tokens "
        f"({total_percent:.2f}% of {BUDGET:,})"
    )

    print("\nSYSTEM PROMPT")
    line_number = 1
    for component in components:
        for part in get_parts(component):
            role, text = get_part_role_and_text(part)
            if role == "system" and text is not None:
                for line in text.splitlines():
                    print(f"{line_number:>4}: {line}")
                    line_number += 1


if __name__ == "__main__":
    main()
