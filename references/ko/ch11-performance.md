# 11장: 성능 (항목 93–103)

3판에서 새로 추가된 장이다.

## 최적화 전에 프로파일링

### 항상 먼저 측정하라
프로파일링 없이 절대 최적화하지 마라. 파이썬 내장 도구:
```python
# 함수 레벨 프로파일링을 위한 cProfile
python -m cProfile -s cumulative my_script.py

# 라인 레벨 프로파일링 (line_profiler 설치 필요)
@profile
def hot_function():
    ...

# 마이크로 벤치마크를 위한 timeit
python -m timeit -s "data = list(range(1000))" "sum(data)"
```

### 80/20 법칙이 적극적으로 적용된다
일반적으로 코드의 5%가 실행 시간의 95%를 차지한다. 그 5%를 찾기 위해 프로파일링하라.
나머지를 최적화하는 것은 헛수고이다.

## 파이썬 레벨 최적화

### 적절한 자료구조 사용
```python
# 나쁨: 리스트에서의 선형 탐색
if item in large_list:  # O(n)

# 좋음: 셋에서의 상수 시간 조회
if item in large_set:  # O(1)

# 올바른 구조 선택:
# - 멤버십 테스트 → set 또는 frozenset
# - 키-값 조회 → dict
# - 순서 있는 시퀀스 → list
# - FIFO 큐 → collections.deque
# - 우선순위 큐 → heapq
# - 정렬된 컬렉션 → bisect와 list 조합
```

### 지역 변수가 전역/속성 조회보다 빠르다
```python
# 타이트한 루프: 속성 조회를 지역 변수에 캐시
def process(items):
    append = result.append  # 메서드 조회 캐시
    for item in items:
        append(transform(item))
```
이것은 매우 핫한 루프에서만 의미가 있다 — 모든 곳에서 하지 마라.

### 문자열 연결
```python
# 나쁨: O(n²) 반복 연결
result = ""
for s in strings:
    result += s

# 좋음: O(n) join
result = "".join(strings)
```

### 메모리 집약적 클래스에는 __slots__ 사용
```python
@dataclass(slots=True)
class Point:
    x: float
    y: float
# 일반 클래스 대비 인스턴스당 ~40-50% 메모리 절감
```

## 내장 가속

### 내장 함수와 연산자 사용
`sum()`, `min()`, `max()`, `sorted()`, `map()`, `filter()`는 C로 구현되어 있고
동등한 파이썬 루프보다 현저히 빠르다.

### 집계에는 리스트 컴프리헨션보다 제너레이터 표현식
```python
# 좋음: 중간 리스트 할당 없음
total = sum(x**2 for x in values)

# 낭비: 합산만 하려고 리스트를 할당
total = sum([x**2 for x in values])
```

## C 확장과 ctypes

### 빠른 네이티브 라이브러리 통합에는 ctypes 고려
```python
import ctypes

libc = ctypes.CDLL("libc.so.6")
result = libc.strlen(b"hello")
```

### 복잡한 경우에는 cffi
ctypes가 다루기 어려워지면, `cffi`가 더 깨끗한 인터페이스를 제공한다.

### 최대 성능을 위한 C 확장 모듈
정말 성능이 중요한 코드에는 C 확장 모듈을 작성하라. 3판에서 이를 깊이 다룬다
— 하지만 먼저 모든 파이썬 레벨 최적화를 소진하라.

**최적화 사다리** (이 순서대로 시도):
1. 더 나은 알고리즘 / 자료구조
2. 내장 함수와 제너레이터
3. 수치 작업에는 NumPy/pandas
4. 핫 루프에는 Cython이나 mypyc
5. 기존 C 라이브러리에는 ctypes/cffi
6. C 확장 모듈 (최후의 수단)

## 핵심 정리
- 최적화 전에 프로파일링 — `cProfile`, `line_profiler`, `timeit`
- 올바른 자료구조 선택 (멤버십에는 set, FIFO에는 deque)
- 문자열 연결에는 `"".join()`, 집계에는 제너레이터 표현식
- 메모리 집약적 객체에는 `__slots__`
- 최적화 사다리 따르기: 알고리즘 → 내장 → NumPy → Cython → C
