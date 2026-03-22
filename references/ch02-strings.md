# Chapter 2: Strings and Slicing (Items 10–16)

## Slicing Fundamentals

### Keep slicing simple and readable
```python
# Good: Clear intent
first_five = items[:5]
last_three = items[-3:]
every_other = items[::2]

# Bad: Avoid start, stop, AND stride together
confusing = items[2:10:3]  # Hard to mentally compute

# Better: Two steps
subset = items[2:10]
result = subset[::3]
```

### Avoid negative stride with start/stop
`items[-2::-2]` is a cognitive puzzle. Split into two operations.
Prefer `reversed()` when you just need reverse iteration.

### Slicing produces copies; assignment mutates
```python
b = a[:]       # Shallow copy
a[2:5] = [10]  # Mutates `a` in place — length can change!
```

### Catch-all unpacking with star expressions
```python
# Extract head/tail patterns cleanly
first, *rest = items
*init, last = items
head, *_, tail = items  # Ignore middle elements
```
Star unpacking always produces a `list`, even if empty. Use it to avoid
manual indexing and off-by-one errors.

## String-Specific Patterns

### Prefer `str.removeprefix()` / `str.removesuffix()` (3.9+)
```python
# Bad: Manual slicing with magic numbers
if s.startswith("test_"):
    name = s[5:]

# Good: Self-documenting
name = s.removeprefix("test_")
```

### Multi-line strings
Use triple-quoted strings with `textwrap.dedent()` for clean multi-line content:
```python
import textwrap
query = textwrap.dedent("""\
    SELECT *
    FROM users
    WHERE active = true
""")
```

## Key Takeaways
- Slice with at most two of (start, stop, stride) at once
- Use star unpacking for variable-length sequences
- Prefer `removeprefix`/`removesuffix` over manual slicing
- `textwrap.dedent` for clean multi-line strings
