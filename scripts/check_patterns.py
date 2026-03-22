#!/usr/bin/env python3
"""Effective Python quick-scan: detect common anti-patterns in Python files.

This script performs a lightweight static analysis pass to flag patterns
that violate Effective Python principles. It's NOT a replacement for
a full review — it catches the obvious stuff so the reviewer can focus
on design-level concerns.

Usage:
    python check_patterns.py <file_or_directory>
    python check_patterns.py src/mypackage/
"""

import ast
import sys
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Finding:
    file: str
    line: int
    rule: str
    message: str
    severity: str  # "critical", "warning", "suggestion"


class EffectivePythonChecker(ast.NodeVisitor):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.findings: list[Finding] = []

    def _add(self, node: ast.AST, rule: str, msg: str, severity: str = "warning") -> None:
        self.findings.append(Finding(self.filename, node.lineno, rule, msg, severity))

    # --- Mutable default arguments (Item 39) ---
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        for default in node.args.defaults + node.args.kw_defaults:
            if default is None:
                continue
            if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                self._add(
                    default,
                    "mutable-default",
                    f"Mutable default argument in '{node.name}()'. Use None sentinel pattern.",
                    "critical",
                )
        # Check for missing return type annotation
        if not node.returns and not node.name.startswith("_"):
            self._add(
                node,
                "missing-return-type",
                f"Public function '{node.name}()' has no return type annotation.",
                "suggestion",
            )
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    # --- Bare except (Item 83) ---
    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        if node.type is None:
            self._add(
                node,
                "bare-except",
                "Bare 'except:' catches everything including KeyboardInterrupt. Catch specific exceptions.",
                "critical",
            )
        self.generic_visit(node)

    # --- range(len(...)) instead of enumerate (Item 17) ---
    def visit_Call(self, node: ast.Call) -> None:
        if (
            isinstance(node.func, ast.Name)
            and node.func.id == "range"
            and len(node.args) == 1
        ):
            arg = node.args[0]
            if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == "len":
                self._add(
                    node,
                    "range-len",
                    "Use 'enumerate()' instead of 'range(len(...))' for index+value iteration.",
                    "warning",
                )
        # Check for print() usage (prefer logging)
        if isinstance(node.func, ast.Name) and node.func.id == "print":
            self._add(
                node,
                "print-usage",
                "Consider using 'logging' instead of 'print()' for production code.",
                "suggestion",
            )
        self.generic_visit(node)

    # --- String concatenation in loop (Item: Performance) ---
    def visit_AugAssign(self, node: ast.AugAssign) -> None:
        if isinstance(node.op, ast.Add) and isinstance(node.target, ast.Name):
            # Heuristic: += on a string variable inside a for loop
            # We can't fully type-check, but flag += with string literals
            if isinstance(node.value, (ast.Constant,)) and isinstance(node.value.value, str):
                self._add(
                    node,
                    "string-concat-loop",
                    "String concatenation with += may be O(n²). Consider ''.join() or list.append().",
                    "warning",
                )
        self.generic_visit(node)

    # --- isinstance checks with multiple types should use tuple (Style) ---
    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        if isinstance(node.op, ast.Or):
            isinstance_calls = [
                v for v in node.values
                if isinstance(v, ast.Call)
                and isinstance(v.func, ast.Name)
                and v.func.id == "isinstance"
            ]
            if len(isinstance_calls) >= 2:
                self._add(
                    node,
                    "isinstance-chain",
                    "Multiple isinstance() calls can be combined: isinstance(x, (TypeA, TypeB)).",
                    "suggestion",
                )
        self.generic_visit(node)


def check_file(path: Path) -> list[Finding]:
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
    except (SyntaxError, UnicodeDecodeError) as e:
        return [Finding(str(path), 0, "parse-error", str(e), "critical")]

    checker = EffectivePythonChecker(str(path))
    checker.visit(tree)
    return checker.findings


def check_path(target: Path) -> list[Finding]:
    findings: list[Finding] = []
    if target.is_file():
        findings.extend(check_file(target))
    elif target.is_dir():
        for py_file in sorted(target.rglob("*.py")):
            if ".venv" in py_file.parts or "node_modules" in py_file.parts:
                continue
            findings.extend(check_file(py_file))
    return findings


SEVERITY_EMOJI = {"critical": "🔴", "warning": "🟡", "suggestion": "🟢"}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python check_patterns.py <file_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1])
    if not target.exists():
        print(f"Error: {target} does not exist")
        sys.exit(1)

    findings = check_path(target)

    if not findings:
        print("✅ No anti-patterns detected. Nice work!")
        sys.exit(0)

    # Group by severity
    for severity in ("critical", "warning", "suggestion"):
        group = [f for f in findings if f.severity == severity]
        if not group:
            continue
        emoji = SEVERITY_EMOJI[severity]
        print(f"\n{emoji} {severity.upper()} ({len(group)})")
        print("=" * 60)
        for f in group:
            print(f"  {f.file}:{f.line} [{f.rule}]")
            print(f"    {f.message}")

    critical = sum(1 for f in findings if f.severity == "critical")
    print(f"\nTotal: {len(findings)} findings ({critical} critical)")
    sys.exit(1 if critical > 0 else 0)


if __name__ == "__main__":
    main()
