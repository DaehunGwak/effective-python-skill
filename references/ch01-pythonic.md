# Chapter 1: Pythonic Thinking (Items 1–16)

Core philosophy: Write Python that leverages the language's unique strengths.
Python has a "canonical" way to do most things — learn it and follow it.

## Version and Style Foundations

- Always know your Python version (`python3 --version`). Target 3.10+ for modern features.
- Follow PEP 8 rigorously: 4-space indentation, snake_case for functions/variables,
  PascalCase for classes, UPPER_CASE for module-level constants.
- Use a formatter (black, ruff format) to eliminate style debates.
- Python is dynamically typed — don't expect compile-time safety. Use type hints +
  mypy/pyright as your "compiler."

## Expressions and Assignments

### Helper functions over complex expressions
```python
# Bad: Dense, hard to debug
result = (value if value > 0 else 0) * rate if rate else default

# Good: Named intermediate steps
clamped = max(value, 0)
result = clamped * rate if rate else default
```

When an expression nests ternary operators or combines multiple boolean conditions,
extract a helper function. The function name documents the intent.

### Unpacking over indexing
```python
# Bad: Positional indexing is fragile and unclear
name = record[0]
age = record[1]

# Good: Unpacking communicates structure
name, age = record

# Good: Star unpacking for variable-length sequences
first, *middle, last = scores
```

### Single-element tuple safety
Always wrap single-element tuples in parentheses to prevent silent bugs:
```python
values = (1,)  # Tuple — clear
values = 1,    # Also tuple, but easy to miss the comma
```

### Conditional expressions
Use inline `if`/`else` only when the result is simple and readable.
If either branch has side effects or is complex, use a full `if` block.

### Walrus operator (:=)
Use assignment expressions to avoid redundant calls, especially in `while` loops
and comprehension filters:
```python
# Good: Compute once, use twice
if (n := len(data)) > 10:
    print(f"Processing {n} items")

# Good: In comprehension filters
results = [y for x in data if (y := transform(x)) is not None]
```
Avoid walrus in places where it hurts readability. If the line is already complex,
use a separate assignment.

### Match/case for destructuring
Use `match`/`case` when destructuring data with known shapes (JSON responses,
command objects, AST nodes). Avoid it as a replacement for simple `if`/`elif`
chains on scalar values — that's not where it shines.
```python
# Good: Structural matching
match command:
    case {"action": "move", "direction": str(d)}:
        move(d)
    case {"action": "quit"}:
        shutdown()
    case _:
        raise ValueError(f"Unknown command: {command}")
```

## Strings and Formatting

### f-strings over format() and %
f-strings are the most readable and fastest string interpolation.
Use them unless you need deferred formatting (logging, i18n).
```python
# Good
print(f"Hello, {name}! You have {count:,} items.")

# When deferred formatting is needed
logger.info("Processing %s items", count)  # Avoid f-string in logging
```

### repr() in f-strings for debugging
Use `!r` for debug output to distinguish types:
```python
print(f"Value: {x!r}")  # Shows quotes around strings, distinguishes None from "None"
```

## Bytes vs Strings

- `str` for text (Unicode), `bytes` for binary data. Never mix them.
- Encode/decode at I/O boundaries only, using explicit encoding (prefer `utf-8`).
- Write helper functions for encoding/decoding when working at boundaries.

## Key Takeaways
- Extract complexity into well-named helper functions
- Use unpacking, walrus, and match/case to reduce noise — but not at the cost of clarity
- f-strings for formatting, explicit encoding at boundaries
- Let tools (formatters, type checkers) enforce mechanical style
