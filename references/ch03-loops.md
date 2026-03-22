# Chapter 3: Loops and Iterators (Items 17–24)

## Prefer enumerate Over range

When you need both index and value, `enumerate` is always clearer than `range(len(...))`:
```python
# Bad
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# Good
for i, item in enumerate(items):
    print(f"{i}: {item}")

# Good: Custom start index
for rank, player in enumerate(leaderboard, start=1):
    print(f"#{rank}: {player}")
```

## Use zip for Parallel Iteration

```python
# Good: Process two sequences in lockstep
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# Use strict=True (3.10+) to catch length mismatches
for name, score in zip(names, scores, strict=True):
    process(name, score)
```
`zip` stops at the shortest iterable by default. Use `itertools.zip_longest`
when you need all elements with a fill value.

## Avoid else Blocks After Loops

The `else` clause on `for`/`while` runs when the loop completes without `break`.
This behavior confuses almost everyone. Instead, use a flag variable or extract
the search into a function that returns early:
```python
# Bad: Confusing else-on-for
for item in items:
    if matches(item):
        break
else:
    handle_not_found()

# Good: Extract to function
def find_match(items):
    for item in items:
        if matches(item):
            return item
    return None

result = find_match(items)
if result is None:
    handle_not_found()
```

## Never Use Loop Variables After the Loop Ends

Loop variables leak into the enclosing scope in Python. This is a language quirk,
not a feature to rely on. Assign the result explicitly within the loop:
```python
# Bad: Relies on leaked variable
for i, item in enumerate(items):
    if item == target:
        break
print(f"Found at {i}")  # What if items is empty?

# Good: Explicit result
found_index = None
for i, item in enumerate(items):
    if item == target:
        found_index = i
        break
```

## Be Defensive When Iterating Over Arguments

If a function iterates over its argument multiple times, it will silently produce
no results on the second pass if given a generator. Defend against this:
```python
# Good: Materialize if you need multiple passes
def analyze(data):
    data = list(data)  # Safe for generators
    total = sum(data)
    return [x / total for x in data]

# Better: Accept a container type explicitly
def analyze(data: Sequence[float]) -> list[float]:
    total = sum(data)
    return [x / total for x in data]
```

## Never Modify Containers While Iterating

Modifying a list/dict/set during iteration causes subtle bugs or `RuntimeError`:
```python
# Bad: Modifying during iteration
for key in d:
    if should_remove(key):
        del d[key]  # RuntimeError!

# Good: Build a list of keys to remove
to_remove = [k for k in d if should_remove(k)]
for key in to_remove:
    del d[key]

# Good: Create a new dict
d = {k: v for k, v in d.items() if not should_remove(k)}
```

## Use any() and all() with Generators

Short-circuit evaluation makes `any`/`all` with generator expressions very efficient:
```python
# Good: Stops at first True
has_negative = any(x < 0 for x in values)

# Good: Stops at first False
all_valid = all(is_valid(item) for item in items)
```
Do not pass a materialized list — the generator form avoids allocating the full list.

## Consider itertools for Complex Iteration

Key functions to know:
- `chain.from_iterable()` — flatten nested iterables
- `islice()` — slice any iterable (not just sequences)
- `groupby()` — group consecutive elements (data must be pre-sorted)
- `product()`, `combinations()`, `permutations()` — combinatorial iteration
- `accumulate()` — running totals or custom accumulations
- `batched()` (3.12+) — chunk iterable into fixed-size groups

```python
from itertools import chain, batched

# Flatten nested lists
flat = list(chain.from_iterable(nested))

# Process in chunks
for batch in batched(items, 100):
    process_batch(batch)
```

## Key Takeaways
- `enumerate` > `range(len(...))`, `zip(strict=True)` for parallel iteration
- Extract loop-with-break patterns into functions with early return
- Never rely on leaked loop variables, never mutate during iteration
- `any()`/`all()` with generators for short-circuit checks
- `itertools` for everything else — avoid reinventing iteration wheels
