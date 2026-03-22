---
name: effective-python
description: >
  Apply Effective Python 3rd Edition principles (Brett Slatkin, 125 items) to write
  idiomatic, high-quality Python code. Covers Pythonic thinking, modern syntax (3.13+),
  comprehensions, generators, functions, classes, metaclasses, concurrency, robustness,
  performance, testing, and collaboration patterns. Use this skill whenever writing,
  reviewing, or refactoring Python code — even if the user doesn't explicitly mention
  "Effective Python." Trigger on: Python code generation, Python code review, Python
  refactoring, "make this more Pythonic", "improve my Python", type hints, async Python,
  error handling patterns, Python best practices, dataclasses, generators, decorators,
  Python performance, or any request involving Python code quality.
---

# Effective Python — Code Quality Skill

Apply the principles from "Effective Python: 125 Specific Ways to Write Better Python"
(Brett Slatkin, 3rd Edition) to produce idiomatic, maintainable, high-performance Python.

> **Copyright note**: This skill encodes *principles and patterns* inspired by the book,
> expressed in original language. It does not reproduce the book's text. Developers are
> encouraged to purchase the book for full explanations and context.

## How This Skill Works

This skill uses **progressive disclosure** across chapter-specific reference files.
The SKILL.md you're reading now contains:
1. A routing table mapping code concerns → reference files
2. Universal principles that apply to ALL Python code
3. A review checklist for comprehensive code audits

**Reference files** in `references/` contain detailed per-chapter guidance.
Load ONLY the reference files relevant to the current task.

## Routing Table — Which Reference to Load

| If the task involves...                            | Load reference file               |
|----------------------------------------------------|-----------------------------------|
| Syntax style, expressions, unpacking, match/case   | `references/ch01-pythonic.md`     |
| Strings, bytes, encoding, slicing                  | `references/ch02-strings.md`     |
| Loops, iterators, enumerate, zip, itertools        | `references/ch03-loops.md`       |
| Dictionaries, defaultdict, __missing__             | `references/ch04-dicts.md`       |
| Comprehensions, generators, yield                  | `references/ch05-generators.md`  |
| Function signatures, decorators, closures          | `references/ch06-functions.md`   |
| Classes, dataclasses, inheritance, interfaces      | `references/ch07-classes.md`     |
| Metaclasses, __init_subclass__, descriptors        | `references/ch08-metaclasses.md` |
| Threading, asyncio, parallelism, concurrency       | `references/ch09-concurrency.md` |
| Error handling, robustness, defensive coding       | `references/ch10-robustness.md`  |
| Performance, profiling, optimization, C-extensions | `references/ch11-performance.md` |
| Testing, debugging, pytest, assertions             | `references/ch12-testing.md`     |
| Packaging, imports, docstrings, collaboration      | `references/ch13-collab.md`      |

**For code generation**: Load 1–3 most relevant references based on the task.
**For code review** (`/effective-python` invocation): Load all relevant references
for the code being reviewed and apply the full checklist below.

## Universal Principles (Always Apply)

These principles cut across all chapters and should inform every line of Python you write:

### 1. Clarity Over Cleverness
Write code that communicates intent. If a one-liner requires mental gymnastics to parse,
break it into named intermediate steps. Helper functions with descriptive names are
almost always better than complex expressions.

### 2. Modern Python (3.10+) Idioms
- Use `X | Y` union syntax for types, not `Union[X, Y]`
- Use `x | None` instead of `Optional[x]`
- Use `match`/`case` for structural pattern matching where it clarifies intent
- Use native type hints (`list[str]`, `dict[str, int]`) instead of `typing` imports
- Use walrus operator (`:=`) to eliminate redundant computations, not to show off
- Use `@dataclass` or `NamedTuple` instead of raw tuples/dicts for structured data

### 3. Fail Fast, Fail Loudly
- Raise exceptions instead of returning `None` for error conditions
- Use specific exception types, never bare `except:`
- Validate inputs at boundaries, trust data internally
- Use `assert` for invariants during development

### 4. Composition Over Inheritance
- Prefer composition and delegation over deep inheritance hierarchies
- Use mix-ins for horizontal functionality sharing
- Use `__init_subclass__` for registration patterns instead of metaclasses
- Use `Protocol` (structural typing) for interface definitions

### 5. Explicit Resource Management
- Always use `with` statements for resources (files, locks, connections)
- Implement `__enter__`/`__exit__` for custom resource types
- Use `contextlib.contextmanager` for simple cases

## Code Review Checklist

When explicitly asked to review Python code, work through these categories systematically.
Load the relevant reference file for each category that applies:

1. **Pythonic Style** — Are modern idioms used? (ch01, ch02)
2. **Data Structures** — Right choice of dict/list/set/tuple/dataclass? (ch04, ch07)
3. **Iteration** — Generators where possible? No mutation during iteration? (ch03, ch05)
4. **Function Design** — Clear signatures? Keyword-only args? No mutable defaults? (ch06)
5. **Class Design** — Appropriate use of inheritance? Composition preferred? (ch07, ch08)
6. **Concurrency** — Thread-safe? Async where beneficial? (ch09)
7. **Robustness** — Proper error handling? Defensive coding at boundaries? (ch10)
8. **Performance** — Obvious inefficiencies? Premature optimization avoided? (ch11)
9. **Testability** — Dependencies injectable? Pure functions where possible? (ch12)
10. **Collaboration** — Docstrings? Type hints? Clean imports? (ch13)

For each issue found, report:
- **What**: The specific code pattern
- **Why**: Why it matters (correctness, readability, performance, or maintainability)
- **How**: The recommended fix with a concrete code example

## Usage Modes

### Auto Mode (during code generation)
When generating Python code, automatically apply the universal principles above
and load 1–2 relevant reference files based on the code being written.
Do not announce that you're using this skill — just write good Python.

### Review Mode (`/effective-python [path]`)
Perform a comprehensive review of the specified code against the full checklist.
Load all relevant reference files. Output a structured review with findings
grouped by severity: 🔴 Critical → 🟡 Suggestion → 🟢 Good Practice Spotted.

### Refactor Mode (`/effective-python refactor [path]`)
Apply the principles to refactor existing code. Show before/after with explanations
referencing the relevant principle.
