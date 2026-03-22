# Chapter 11: Performance (Items 93–103)

Another new chapter in the 3rd edition.

## Profiling Before Optimizing

### Always measure first
Never optimize without profiling. Python's built-in tools:
```python
# cProfile for function-level profiling
python -m cProfile -s cumulative my_script.py

# Line-level profiling (install line_profiler)
@profile
def hot_function():
    ...

# timeit for micro-benchmarks
python -m timeit -s "data = list(range(1000))" "sum(data)"
```

### The 80/20 rule applies aggressively
Typically, 5% of code accounts for 95% of runtime. Profile to find that 5%.
Optimizing anything else is wasted effort.

## Python-Level Optimizations

### Use appropriate data structures
```python
# Bad: Linear search in list
if item in large_list:  # O(n)

# Good: Constant-time lookup in set
if item in large_set:  # O(1)

# Choosing the right structure:
# - Membership testing → set or frozenset
# - Key-value lookup → dict
# - Ordered sequence → list
# - FIFO queue → collections.deque
# - Priority queue → heapq
# - Sorted collection → bisect with list
```

### Local variables are faster than global/attribute lookups
```python
# Tight loops: cache attribute lookups in local variables
def process(items):
    append = result.append  # Cache method lookup
    for item in items:
        append(transform(item))
```
This matters only in very hot loops — don't do it everywhere.

### String concatenation
```python
# Bad: O(n²) repeated concatenation
result = ""
for s in strings:
    result += s

# Good: O(n) join
result = "".join(strings)
```

### Use __slots__ for memory-heavy classes
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
# ~40-50% less memory per instance vs regular class
```

## Built-in Acceleration

### Use built-in functions and operators
`sum()`, `min()`, `max()`, `sorted()`, `map()`, `filter()` are implemented in C and
are significantly faster than equivalent Python loops.

### Generator expressions over list comprehensions for aggregation
```python
# Good: No intermediate list allocation
total = sum(x**2 for x in values)

# Wasteful: Allocates a list just to sum it
total = sum([x**2 for x in values])
```

## C Extensions and ctypes

### Consider ctypes for quick native library integration
```python
import ctypes

libc = ctypes.CDLL("libc.so.6")
result = libc.strlen(b"hello")
```

### cffi for more complex cases
When ctypes becomes unwieldy, `cffi` provides a cleaner interface.

### C extension modules for maximum performance
For truly performance-critical code, write a C extension module. The 3rd edition
covers this in depth — but first exhaust all Python-level optimizations.

**Optimization ladder** (try in this order):
1. Better algorithm / data structure
2. Built-in functions and generators
3. NumPy/pandas for numerical work
4. Cython or mypyc for hot loops
5. ctypes/cffi for existing C libraries
6. C extension module (last resort)

## Key Takeaways
- Profile before optimizing — `cProfile`, `line_profiler`, `timeit`
- Choose the right data structure (set for membership, deque for FIFO)
- `"".join()` for string concatenation, generator expressions for aggregation
- `__slots__` for memory-heavy objects
- Follow the optimization ladder: algorithm → built-ins → NumPy → Cython → C
