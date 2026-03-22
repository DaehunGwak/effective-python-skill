# Chapter 5: Comprehensions and Generators (Items 30–36)

## Comprehension Principles

### Limit nesting to two levels
```python
# Good: Single comprehension
squares = [x**2 for x in range(10)]

# Acceptable: Two levels (flat matrix traversal)
flat = [cell for row in matrix for cell in row]

# Bad: Three levels — use a loop instead
result = [f(x, y, z) for x in xs for y in ys for z in zs if pred(x, y, z)]
```
The rule of thumb: if a comprehension requires more than two `for` clauses or
contains complex conditions, rewrite it as an explicit loop. Readability wins.

### Use multiple assignments in comprehensions (walrus)
```python
# Good: Compute once, filter and transform
results = [
    transformed
    for x in data
    if (transformed := expensive_transform(x)) is not None
]
```

### Generator expressions for single-pass large data
```python
# Good: Lazy evaluation, low memory
total = sum(len(line) for line in file)

# Good: Chain generator expressions
roots = (x**0.5 for x in values)
rounded = (round(r, 2) for r in roots)
```

### Prefer dict/set comprehensions over dict()/set() with generators
```python
# Good
lookup = {item.id: item for item in items}
unique_categories = {item.category for item in items}
```

## Generators (yield)

### Use generators instead of returning lists
When a function builds a list and returns it, consider whether a generator is more
appropriate. Generators are better when:
- The full list may not fit in memory
- The caller may only need part of the results
- Results can be produced incrementally

```python
# Bad: Builds entire list in memory
def read_records(path: str) -> list[Record]:
    results = []
    with open(path) as f:
        for line in f:
            results.append(parse(line))
    return results

# Good: Yields one at a time
def read_records(path: str) -> Iterator[Record]:
    with open(path) as f:
        for line in f:
            yield parse(line)
```

### yield from for delegation
Use `yield from` to delegate to sub-generators cleanly:
```python
def walk_tree(node):
    yield node.value
    for child in node.children:
        yield from walk_tree(child)
```

### send() and throw() — use sparingly
`generator.send()` enables coroutine-style communication but makes code hard to
follow. Prefer passing callbacks or using `asyncio` for complex data flows.
Only use `send()` when you need bidirectional streaming (e.g., data pipelines).

### Use itertools.islice for generator slicing
Generators don't support indexing. Use `itertools.islice`:
```python
from itertools import islice

first_10 = list(islice(infinite_generator(), 10))
```

## Key Takeaways
- Comprehensions: max 2 `for` clauses, use walrus for compute-once-filter
- Generator expressions for single-pass, large-data aggregations
- `yield` instead of building and returning lists when data is large or streamed
- `yield from` for clean sub-generator delegation
- Avoid `send()`/`throw()` unless you have a clear need for bidirectional streaming
