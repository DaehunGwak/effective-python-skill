# 9장: 동시성과 병렬 처리 (항목 72–82)

## GIL 이해하기

전역 인터프리터 잠금(GIL)은 한 번에 하나의 스레드만 Python 바이트코드를 실행할 수 있게 한다.
이것은 중요한 의미를 갖는다:
- **CPU 바운드 작업**: 스레드는 병렬성을 제공하지 않는다. `multiprocessing`이나
  `ProcessPoolExecutor`를 사용하라.
- **I/O 바운드 작업**: I/O 대기 중 GIL이 해제되므로 스레드가 잘 동작한다.
  높은 동시성 I/O에는 `asyncio`가 더 낫다.
- Python 3.13+에는 실험적인 자유 스레딩(no-GIL) 모드가 있지만, 아직 주류는 아니다.

## 스레딩

### 블로킹 I/O에는 스레드 사용
```python
from concurrent.futures import ThreadPoolExecutor

def fetch_url(url: str) -> str:
    return requests.get(url).text

with ThreadPoolExecutor(max_workers=10) as pool:
    results = list(pool.map(fetch_url, urls))
```

### 스레드 안전한 변경에는 Lock 사용
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
스레드 안전성을 GIL에 의존하지 마라 — 복합 연산(읽기-수정-쓰기)에서
데이터 레이스는 여전히 가능하다.

### 스레드 통신에는 Queue 사용
```python
from queue import Queue
from threading import Thread

def producer(q: Queue) -> None:
    for item in generate_items():
        q.put(item)
    q.put(None)  # 센티널

def consumer(q: Queue) -> None:
    while (item := q.get()) is not None:
        process(item)
```

## asyncio

### 높은 동시성 I/O에는 async/await 사용
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

### TaskGroup으로 구조화된 동시성 (3.11+)
```python
async def process_all(items: list[Item]) -> list[Result]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_item(item))
    return results
```
`TaskGroup`은 어떤 태스크가 예외를 발생시키면 나머지 태스크를 자동으로 취소한다.
더 나은 에러 처리를 위해 bare `asyncio.gather`보다 선호하라.

### 동기와 비동기를 절대 순진하게 섞지 마라
- 이미 실행 중인 이벤트 루프 안에서 `asyncio.run()`을 호출하지 마라
- async 컨텍스트에서 블로킹 코드를 실행하려면 `asyncio.to_thread()`를 사용하라
- 레거시 동기 라이브러리에는 `loop.run_in_executor()`를 사용하라

```python
# 좋음: async에서 블로킹 코드를 스레드에서 실행
async def read_file(path: str) -> str:
    return await asyncio.to_thread(Path(path).read_text)
```

## CPU 바운드 작업에는 멀티프로세싱

```python
from concurrent.futures import ProcessPoolExecutor

def compute_heavy(data: bytes) -> float:
    # CPU 집약적 작업
    return result

with ProcessPoolExecutor() as pool:
    results = list(pool.map(compute_heavy, data_chunks))
```

주의: 인자와 반환값은 pickle 가능해야 한다. 시작 비용이 높다 —
작은 태스크에는 프로세스를 사용하지 마라.

## 핵심 정리
- I/O 바운드에는 스레드, CPU 바운드에는 프로세스, 높은 동시성 I/O에는 asyncio
- 스레드에서 공유 가변 상태에는 항상 `Lock` 사용
- 에러 안전성을 위해 bare `gather`보다 `asyncio.TaskGroup` (3.11+)
- 동기 코드를 async로 브릿지하려면 `asyncio.to_thread()`
- 스레드 간 통신에는 `Queue`
- GIL은 스레드가 Python 계산을 병렬화하지 않음을 의미
