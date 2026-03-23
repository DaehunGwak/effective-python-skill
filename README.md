# 🐍 Effective Python — Claude Code Skill

> Apply [Effective Python 3rd Edition](https://effectivepython.com/) (Brett Slatkin, 125 items) principles automatically when writing, reviewing, or refactoring Python code with [Claude Code](https://code.claude.com/).

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Claude Code Skill](https://img.shields.io/badge/claude--code-skill-blueviolet.svg)](https://code.claude.com/docs/en/skills)
[![Install with skills.sh](https://img.shields.io/badge/skills.sh-install-blue)](https://skills.sh)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<div align="center">

Translations: [한국어](https://github.com/DaehunGwak/effective-python-skill/blob/translation/ko/README.ko.md)

</div>

## Why This Skill?

Claude Code already writes decent Python — but "decent" isn't "Pythonic." This skill encodes the **125 battle-tested principles** from Brett Slatkin's Effective Python so Claude Code consistently produces idiomatic, maintainable, high-performance code.

**Without this skill**, Claude might:
- Use `range(len(items))` instead of `enumerate`
- Return `None` for errors instead of raising exceptions
- Use mutable default arguments
- Build deep inheritance hierarchies instead of composition

**With this skill**, Claude Code follows Effective Python principles by default.

## Quick Install

### Via skills.sh (Recommended)

```bash
npx skills add DaehunGwak/effective-python-skill
```

### Via git clone

```bash
# Project-level
git clone https://github.com/DaehunGwak/effective-python-skill.git .claude/skills/effective-python-3e

# Global (all projects)
git clone https://github.com/DaehunGwak/effective-python-skill.git ~/.claude/skills/effective-python-3e
```

### Via install script

```bash
curl -sSL https://raw.githubusercontent.com/DaehunGwak/effective-python-skill/main/install.sh | bash
```

## Usage

### Auto Mode — Just Write Python

Once installed, the skill activates automatically when Claude Code generates Python.
No commands needed — just ask Claude to write code and it applies Effective Python principles.

### Review Mode — Audit Existing Code

```
/effective-python-3e src/mypackage/
```

Performs a comprehensive review against the Effective Python checklist:

```
🔴 CRITICAL — src/api/handler.py:42
   Mutable default argument: def process(items, cache={})
   → Use None sentinel: def process(items, cache=None)

🟡 SUGGESTION — src/models/user.py:15
   Returning None for errors. Raise UserNotFoundError instead.
   → Callers can't confuse "not found" with falsy values.

🟢 GOOD — src/utils/transform.py:8
   Clean use of generator expression with itertools.chain
```

### Refactor Mode — Modernize Code

```
/effective-python-3e refactor src/legacy_module.py
```

Shows before/after with references to which Effective Python principle applies.

### Static Analysis Script

Quick AST-based scan for common anti-patterns:

```bash
python .claude/skills/effective-python-3e/scripts/check_patterns.py src/
```

Detects: mutable defaults, bare except, `range(len())`, string concatenation in loops,
missing type annotations, `isinstance` chains, and more.

## Architecture

```
effective-python-3e/
├── SKILL.md                    # Orchestrator with routing table (126 lines)
├── references/                 # Chapter-specific guidelines (lazy-loaded)
│   ├── ch01-pythonic.md       # Pythonic Thinking — syntax, expressions, style
│   ├── ch02-strings.md       # Strings, bytes, slicing
│   ├── ch03-loops.md         # Loops, iterators, enumerate, zip, itertools
│   ├── ch04-dicts.md         # Dictionaries, defaultdict, __missing__
│   ├── ch05-generators.md    # Comprehensions, generators, yield
│   ├── ch06-functions.md     # Signatures, decorators, closures
│   ├── ch07-classes.md       # Dataclasses, composition, interfaces
│   ├── ch08-metaclasses.md   # __init_subclass__, descriptors
│   ├── ch09-concurrency.md   # Threading, asyncio, parallelism
│   ├── ch10-robustness.md    # Error handling, defensive coding (NEW in 3rd ed)
│   ├── ch11-performance.md   # Profiling, optimization (NEW in 3rd ed)
│   ├── ch12-testing.md       # pytest, debugging, coverage
│   └── ch13-collab.md       # Packaging, docstrings, type hints
├── scripts/
│   └── check_patterns.py      # AST-based anti-pattern detector
├── install.sh                  # One-command installer
├── LICENSE
└── README.md
```

### Progressive Disclosure Pattern

This skill handles 125 items without overwhelming the context window:

| Layer | Size | When Loaded |
|-------|------|-------------|
| Metadata (name + description) | ~100 tokens | Always in context |
| SKILL.md body (routing + universal rules) | 126 lines | When skill triggers |
| Reference files (per-chapter) | 67–172 lines each | Only relevant chapters |
| Script (check_patterns.py) | 157 lines | Only on explicit invocation |

During code generation, only 1–2 reference files load. During a full review, relevant chapters load on demand. This keeps token usage efficient while covering all 125 principles.

## What's Covered

| Chapter | Items | Key Principles |
|---------|-------|----------------|
| Pythonic Thinking | 1–16 | f-strings, unpacking, walrus operator, match/case |
| Strings & Slicing | 10–16 | Stride limits, `removeprefix`, bytes/str boundary |
| Loops & Iterators | 17–24 | `enumerate`, `zip(strict=True)`, `itertools`, `any`/`all` |
| Dictionaries | 25–29 | `get()`, `defaultdict`, `__missing__`, nesting limits |
| Comprehensions | 30–36 | Max 2 `for` clauses, generators over lists, `yield from` |
| Functions | 30–44 | Keyword-only args, `None` sentinel, `@wraps`, result objects |
| Classes | 45–60 | Composition > inheritance, `Protocol`, `@dataclass(slots=True)` |
| Metaclasses | 61–71 | `__init_subclass__` over metaclasses, descriptors |
| Concurrency | 72–82 | GIL awareness, `TaskGroup`, `asyncio.to_thread`, `Lock` |
| Robustness | 83–92 | Narrow `try` blocks, exception hierarchies, boundary validation |
| Performance | 93–103 | Profile-first, data structure choice, optimization ladder |
| Testing | 104–115 | pytest fixtures, behavior testing, `breakpoint()`, logging |
| Collaboration | 116–125 | Docstrings, `__all__`, virtual envs, progressive typing |

## Customization

### Add Project-Specific Rules

Create a new reference file and register it in SKILL.md's routing table:

```markdown
# In references/ch-myproject.md
# Project-specific patterns...

# In SKILL.md routing table, add:
| Django views/models | `references/ch-django.md` |
```

### Adjust Severity

Edit the Universal Principles section in SKILL.md to emphasize what matters most to your team.

## Copyright Notice

This skill encodes **principles and patterns inspired by** the book, expressed in original language.
It does not reproduce the book's text. Developers are strongly encouraged to
[purchase Effective Python](https://effectivepython.com/) for full explanations, context, and examples.

## Contributing

1. Fork this repo
2. Add or improve reference files
3. Test with `python scripts/check_patterns.py` on sample code
4. Submit a PR with a description of what principles you've added/improved

## License

MIT — see [LICENSE](LICENSE) for details.
