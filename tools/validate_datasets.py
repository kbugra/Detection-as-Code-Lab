#!/usr/bin/env python3
"""Validate Sigma rules against curated positive and negative datasets."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
VALIDATION_CASES = ROOT / "tests" / "validation_cases.json"


def strip_inline_comment(line: str) -> str:
    in_single = False
    in_double = False

    for index, char in enumerate(line):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            return line[:index].rstrip()

    return line.rstrip()


def parse_scalar(value: str) -> Any:
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return value


def load_simple_yaml(path: Path) -> dict[str, Any]:
    lines: list[tuple[int, str]] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        clean_line = strip_inline_comment(raw_line)
        if not clean_line.strip():
            continue
        indent = len(clean_line) - len(clean_line.lstrip(" "))
        lines.append((indent, clean_line.lstrip()))

    index = 0

    def parse_block(expected_indent: int) -> Any:
        if index >= len(lines):
            raise ValueError(f"Unexpected end of YAML while parsing {path}")

        indent, content = lines[index]
        if indent != expected_indent:
            raise ValueError(
                f"Unexpected indentation in {path}: expected {expected_indent}, got {indent}"
            )

        if content.startswith("- "):
            return parse_list(expected_indent)
        return parse_dict(expected_indent)

    def parse_list(expected_indent: int) -> list[Any]:
        nonlocal index
        items: list[Any] = []

        while index < len(lines):
            indent, content = lines[index]
            if indent != expected_indent or not content.startswith("- "):
                break

            value = content[2:].strip()
            index += 1

            if not value:
                if index < len(lines) and lines[index][0] > expected_indent:
                    items.append(parse_block(lines[index][0]))
                else:
                    items.append(None)
                continue

            if value.endswith(":"):
                key = value[:-1].strip()
                item: dict[str, Any] = {key: None}
                if index < len(lines) and lines[index][0] > expected_indent:
                    item[key] = parse_block(lines[index][0])
                items.append(item)
                continue

            items.append(parse_scalar(value))

        return items

    def parse_dict(expected_indent: int) -> dict[str, Any]:
        nonlocal index
        mapping: dict[str, Any] = {}

        while index < len(lines):
            indent, content = lines[index]
            if indent != expected_indent or content.startswith("- "):
                break

            if ":" not in content:
                raise ValueError(f"Invalid YAML mapping entry in {path}: {content}")

            key, raw_value = content.split(":", 1)
            key = key.strip()
            value = raw_value.strip()
            index += 1

            if value:
                mapping[key] = parse_scalar(value)
                continue

            if index < len(lines) and lines[index][0] > expected_indent:
                mapping[key] = parse_block(lines[index][0])
            else:
                mapping[key] = None

        return mapping

    parsed = parse_block(0)
    if not isinstance(parsed, dict):
        raise ValueError(f"Top-level YAML document must be a mapping: {path}")
    return parsed


def load_events(path: Path) -> list[dict[str, Any]]:
    raw_text = path.read_text(encoding="utf-8").strip()
    if not raw_text:
        return []

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        events = []
        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue
            events.append(json.loads(line))
        return events

    if isinstance(parsed, dict):
        return [parsed]
    if isinstance(parsed, list):
        return parsed
    raise ValueError(f"Unsupported JSON structure in dataset: {path}")


def flatten_event(event: dict[str, Any]) -> dict[str, Any]:
    flattened: dict[str, Any] = {}

    for key, value in event.items():
        if key == "EventData" and isinstance(value, dict):
            for nested_key, nested_value in value.items():
                flattened.setdefault(nested_key, nested_value)
                flattened[f"EventData.{nested_key}"] = nested_value
            continue
        flattened[key] = value

    return flattened


def normalize(value: Any) -> str:
    return str(value).strip().lower()


def ensure_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    return [value]


def match_field(modifiers: list[str], expected: Any, actual: Any) -> bool:
    actual_text = normalize(actual)
    expected_values = [normalize(item) for item in ensure_list(expected)]

    if "contains" in modifiers:
        if "all" in modifiers:
            return all(item in actual_text for item in expected_values)
        return any(item in actual_text for item in expected_values)

    if "startswith" in modifiers:
        return any(actual_text.startswith(item) for item in expected_values)

    if "endswith" in modifiers:
        return any(actual_text.endswith(item) for item in expected_values)

    return any(actual_text == item for item in expected_values)


def evaluate_selection(selection: dict[str, Any], event: dict[str, Any]) -> bool:
    for raw_key, expected in selection.items():
        parts = raw_key.split("|")
        field = parts[0]
        modifiers = parts[1:]
        actual = event.get(field)
        if actual is None:
            return False
        if not match_field(modifiers, expected, actual):
            return False
    return True


IDENTIFIER = re.compile(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b")


def evaluate_condition(condition: str, results: dict[str, bool]) -> bool:
    expression = condition
    tokens = set(IDENTIFIER.findall(condition))

    for token in tokens:
        if token in {"and", "or", "not", "True", "False"}:
            continue
        if token not in results:
            raise ValueError(f"Unsupported condition token: {token}")
        expression = re.sub(rf"\b{re.escape(token)}\b", str(results[token]), expression)

    return bool(eval(expression, {"__builtins__": {}}, {}))


def count_rule_matches(rule_path: Path, dataset_path: Path) -> int:
    rule = load_simple_yaml(rule_path)
    detection = rule["detection"]
    condition = detection["condition"]
    selectors = {key: value for key, value in detection.items() if key != "condition"}

    match_count = 0
    for event in load_events(dataset_path):
        flattened = flatten_event(event)
        selector_results = {
            key: evaluate_selection(value, flattened)
            for key, value in selectors.items()
        }
        if evaluate_condition(condition, selector_results):
            match_count += 1

    return match_count


def main() -> int:
    cases = json.loads(VALIDATION_CASES.read_text(encoding="utf-8"))["cases"]
    failures: list[str] = []

    print("Running Sigma fixture validation...")

    for case in cases:
        rule_path = ROOT / case["rule"]
        print(f"\n[{case['name']}]")
        print(f"Rule: {case['rule']}")

        for positive in case.get("positive", []):
            dataset_path = ROOT / positive["path"]
            matches = count_rule_matches(rule_path, dataset_path)
            minimum = positive["min_matches"]
            print(f"  POS {positive['path']}: {matches} match(es), expected >= {minimum}")
            if matches < minimum:
                failures.append(
                    f"{case['name']} failed positive check for {positive['path']} "
                    f"(got {matches}, expected >= {minimum})"
                )

        for negative in case.get("negative", []):
            dataset_path = ROOT / negative["path"]
            matches = count_rule_matches(rule_path, dataset_path)
            maximum = negative["max_matches"]
            print(f"  NEG {negative['path']}: {matches} match(es), expected <= {maximum}")
            if matches > maximum:
                failures.append(
                    f"{case['name']} failed negative check for {negative['path']} "
                    f"(got {matches}, expected <= {maximum})"
                )

    if failures:
        print("\nValidation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nAll validation cases passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
