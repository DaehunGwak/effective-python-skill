# 5장: 컴프리헨션과 제너레이터 (항목 30–36)

## 컴프리헨션 원칙

### 중첩은 2단계까지 제한
```python
# 좋음: 단일 컴프리헨션
squares = [x**2 for x in range(10)]

# 허용 가능: 2단계 (평탄 행렬 순회)
flat = [cell for row in matrix for cell in row]

# 나쁨: 3단계 — 대신 루프를 사용하라
result = [f(x, y, z) for x in xs for y in ys for z in zs if pred(x, y, z)]
```
경험 법칙: 컴프리헨션에 2개 이상의 `for` 절이 필요하거나
복잡한 조건이 포함되면, 명시적 루프로 다시 작성하라. 가독성이 우선이다.

### 컴프리헨션에서 왈러스로 다중 대입
```python
# 좋음: 한 번 계산하고, 필터링하고, 변환
results = [
    transformed
    for x in data
    if (transformed := expensive_transform(x)) is not None
]
```

### 대용량 데이터의 단일 패스에는 제너레이터 표현식
```python
# 좋음: 지연 평가, 낮은 메모리
total = sum(len(line) for line in file)

# 좋음: 제너레이터 표현식 체이닝
roots = (x**0.5 for x in values)
rounded = (round(r, 2) for r in roots)
```

### dict()/set() + 제너레이터보다 딕셔너리/셋 컴프리헨션 선호
```python
# 좋음
lookup = {item.id: item for item in items}
unique_categories = {item.category for item in items}
```

## 제너레이터 (yield)

### 리스트를 반환하는 대신 제너레이터 사용
함수가 리스트를 구축하고 반환한다면, 제너레이터가 더 적합한지 고려하라.
제너레이터가 더 나은 경우:
- 전체 리스트가 메모리에 들어가지 않을 수 있을 때
- 호출자가 결과의 일부만 필요할 수 있을 때
- 결과를 점진적으로 생산할 수 있을 때

```python
# 나쁨: 전체 리스트를 메모리에 구축
def read_records(path: str) -> list[Record]:
    results = []
    with open(path) as f:
        for line in f:
            results.append(parse(line))
    return results

# 좋음: 한 번에 하나씩 yield
def read_records(path: str) -> Iterator[Record]:
    with open(path) as f:
        for line in f:
            yield parse(line)
```

### 위임에는 yield from
하위 제너레이터에 깔끔하게 위임하려면 `yield from`을 사용하라:
```python
def walk_tree(node):
    yield node.value
    for child in node.children:
        yield from walk_tree(child)
```

### send()와 throw() — 절제하여 사용
`generator.send()`는 코루틴 스타일 통신을 가능하게 하지만 코드를 추적하기 어렵게 한다.
복잡한 데이터 흐름에는 콜백 전달이나 `asyncio` 사용을 선호하라.
양방향 스트리밍(예: 데이터 파이프라인)이 필요할 때만 `send()`를 사용하라.

### 제너레이터 슬라이싱에는 itertools.islice
제너레이터는 인덱싱을 지원하지 않는다. `itertools.islice`를 사용하라:
```python
from itertools import islice

first_10 = list(islice(infinite_generator(), 10))
```

## 핵심 정리
- 컴프리헨션: 최대 2개 `for` 절, 한 번 계산-필터링에 왈러스 사용
- 대용량 단일 패스 집계에는 제너레이터 표현식
- 데이터가 크거나 스트리밍될 때 리스트 구축-반환 대신 `yield`
- 깔끔한 하위 제너레이터 위임에 `yield from`
- 양방향 스트리밍의 명확한 필요가 없다면 `send()`/`throw()` 피하기
