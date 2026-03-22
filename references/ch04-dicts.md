# Chapter 4: Dictionaries (Items 25–29)

## Dictionary Insertion Ordering

Since Python 3.7, dicts preserve insertion order. You can rely on this, but be cautious:
- Don't assume dicts from external sources (JSON, DB results) have a specific order
- If order matters semantically, consider whether an `OrderedDict` makes intent clearer
- Keyword arguments (`**kwargs`) also preserve order

## Handling Missing Keys

### Prefer get() over in + KeyError
```python
# Bad: Two lookups
if key in d:
    value = d[key]
else:
    value = default

# Bad: LBYL + exception handling mixed
try:
    value = d[key]
except KeyError:
    value = default

# Good: Single lookup
value = d.get(key, default)
```

### Use setdefault sparingly
`setdefault` is useful when you want to insert a default AND get the reference
in one call, but the code reads poorly. Prefer `defaultdict` for this pattern:
```python
# Acceptable for one-off cases
d.setdefault(key, []).append(item)

# Better for repeated use: defaultdict
from collections import defaultdict
d = defaultdict(list)
d[key].append(item)
```

### defaultdict for Internal State
Use `defaultdict` when building internal aggregations:
```python
from collections import defaultdict

# Grouping
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)

# Counting (though Counter is even better for this)
counts = defaultdict(int)
for word in words:
    counts[word] += 1

# Better for counting:
from collections import Counter
counts = Counter(words)
```

### __missing__ for Key-Dependent Defaults
When the default value depends on the key itself, `defaultdict` falls short.
Subclass `dict` and implement `__missing__`:
```python
class PictureCache(dict):
    def __missing__(self, key: str) -> bytes:
        value = load_picture(key)
        self[key] = value
        return value

cache = PictureCache()
image = cache["photo.jpg"]  # Loads on first access, cached after
```
This is a clean pattern for lazy-loading caches and configuration lookups.

## Compose Classes Instead of Nesting

When you find yourself nesting dicts 2+ levels deep, it's time for a class:
```python
# Bad: Deeply nested dict
students["Alice"]["grades"]["math"].append(95)

# Good: Compose with dataclasses
@dataclass
class Student:
    name: str
    grades: dict[str, list[int]] = field(default_factory=dict)

    def add_grade(self, subject: str, score: int) -> None:
        self.grades.setdefault(subject, []).append(score)
```

## Key Takeaways
- `dict.get(key, default)` for safe lookups
- `defaultdict` for grouping/counting patterns
- `__missing__` for key-dependent default computation
- When nesting dicts beyond 2 levels, refactor into classes
- `Counter` for frequency counting
