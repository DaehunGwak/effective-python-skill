# Chapter 9: Concurrency and Parallelism (Items 72–82)

## Understanding the GIL

The Global Interpreter Lock means only one thread executes Python bytecode at a time.
This has important implications:
- **CPU-bound work**: Threads do NOT provide parallelism. Use `multiprocessing` or
  `ProcessPoolExecutor`.
- **I/O-bound work**: Threads work fine because the GIL is released during I/O waits.
  `asyncio` is even better for high-concurrency I/O.
- Python 3.13+ has experimental free-threading (no-GIL) mode, but it's not yet mainstream.

## Threading

### Use threads for blocking I/O
```python
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url: str) -> str:
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(fetch_url, urls))
```

### Use Lock for thread-safe mutations
```python
from threading import Lock

class Counter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = Lock()

    def increment(self) -> None:
        with self._lock:
            self._value += 1
```
Never rely on the GIL for thread safety — data races on compound operations
(read-modify-write) are still possible.

### Use Queue for thread communication
```python
from queue import Queue
from threading import Thread

def producer(q: Queue) -> None:
    for item in generate_items():
        q.put(item)
    q.put(None)  # Sentinel

def consumer(q: Queue) -> None:
    while (item := q.get()) is not None:
        process(item)
```

## asyncio

### Use async/await for high-concurrency I/O
```python
import asyncio
import aiohttp

async def fetch(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url) as resp:
        return await resp.text()

async def fetch_all(urls: list[str]) -> list[str]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

### Structured concurrency with TaskGroup (3.11+)
```python
async def process_all(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_item(item))
    return results
```
`TaskGroup` automatically cancels remaining tasks if any task raises an exception.
Prefer it over bare `asyncio.gather` for better error handling.

### Never mix sync and async naively
- Don't call `asyncio.run()` inside an already-running event loop
- Use `asyncio.to_thread()` to run blocking code from async context
- Use `loop.run_in_executor()` for legacy sync libraries

```python
# Good: Run blocking code in a thread from async
async def read_file(path: str) -> str:
    return await asyncio.to_thread(Path(path).read_text)
```

## Multiprocessing for CPU-bound Work

```python
from concurrent.futures import ProcessPoolExecutor

def compute_heavy(data: bytes) -> float:
    # CPU-intensive work
    return result

with ProcessPoolExecutor() as pool:
    results = list(pool.map(compute_heavy, data_chunks))
```

Caveat: Arguments and return values must be picklable. Startup cost is high —
don't use processes for tiny tasks.

## Key Takeaways
- Threads for I/O-bound, processes for CPU-bound, asyncio for high-concurrency I/O
- Always use `Lock` for shared mutable state in threads
- `asyncio.TaskGroup` (3.11+) over bare `gather` for error safety
- `asyncio.to_thread()` to bridge sync code into async
- `Queue` for thread-to-thread communication
- GIL means threads don't parallelize Python computation
