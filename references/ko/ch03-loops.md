# 3장: 반복문과 이터레이터 (항목 17–24)

## range 대신 enumerate 선호

인덱스와 값이 모두 필요할 때, `enumerate`는 항상 `range(len(...))`보다 명확하다:
```python
# 나쁨
for i in range(len(items)):
    print(f"{i}: {items[i]}")

# 좋음
for i, item in enumerate(items):
    print(f"{i}: {item}")

# 좋음: 시작 인덱스 커스텀
for rank, player in enumerate(leaderboard, start=1):
    print(f"#{rank}: {player}")
```

## 병렬 순회에는 zip 사용

```python
# 좋음: 두 시퀀스를 동기적으로 처리
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# 길이 불일치를 잡기 위해 strict=True 사용 (3.10+)
for name, score in zip(names, scores, strict=True):
    process(name, score)
```
`zip`은 기본적으로 가장 짧은 이터러블에서 멈춘다.
채움 값으로 모든 요소가 필요하면 `itertools.zip_longest`를 사용하라.

## 반복문 뒤의 else 블록 피하기

`for`/`while`의 `else` 절은 `break` 없이 루프가 완료될 때 실행된다.
이 동작은 거의 모든 사람을 혼란스럽게 한다. 대신 플래그 변수를 사용하거나
조기 반환하는 함수로 검색 로직을 추출하라:
```python
# 나쁨: 혼란스러운 for-else
for item in items:
    if matches(item):
        break
else:
    handle_not_found()

# 좋음: 함수로 추출
def find_match(items):
    for item in items:
        if matches(item):
            return item
    return None

result = find_match(items)
if result is None:
    handle_not_found()
```

## 루프 종료 후 루프 변수를 절대 사용하지 마라

파이썬에서 루프 변수는 둘러싼 스코프로 누출된다. 이것은 언어의 특이점이지,
의존할 기능이 아니다. 루프 내에서 결과를 명시적으로 대입하라:
```python
# 나쁨: 누출된 변수에 의존
for i, item in enumerate(items):
    if item == target:
        break
print(f"{i}번째에서 찾음")  # items가 비어있으면?

# 좋음: 명시적 결과
found_index = None
for i, item in enumerate(items):
    if item == target:
        found_index = i
        break
```

## 인자 순회 시 방어적으로 코딩하라

함수가 인자를 여러 번 순회하는 경우, 제너레이터가 전달되면 두 번째 패스에서
조용히 아무 결과도 생성하지 않는다. 이에 대비하라:
```python
# 좋음: 여러 패스가 필요하면 실체화
def analyze(data):
    data = list(data)  # 제너레이터에 안전
    total = sum(data)
    return [x / total for x in data]

# 더 나음: 컨테이너 타입을 명시적으로 받기
def analyze(data: Sequence[float]) -> list[float]:
    total = sum(data)
    return [x / total for x in data]
```

## 순회 중 절대 컨테이너를 수정하지 마라

순회 중 리스트/딕셔너리/셋을 수정하면 미묘한 버그나 `RuntimeError`가 발생한다:
```python
# 나쁨: 순회 중 수정
for key in d:
    if should_remove(key):
        del d[key]  # RuntimeError!

# 좋음: 제거할 키 목록을 먼저 만들기
to_remove = [k for k in d if should_remove(k)]
for key in to_remove:
    del d[key]

# 좋음: 새 딕셔너리 생성
d = {k: v for k, v in d.items() if not should_remove(k)}
```

## 제너레이터와 함께 any()와 all() 사용

단락 평가(short-circuit)로 `any`/`all`과 제너레이터 표현식의 조합은 매우 효율적이다:
```python
# 좋음: 첫 번째 True에서 멈춤
has_negative = any(x < 0 for x in values)

# 좋음: 첫 번째 False에서 멈춤
all_valid = all(is_valid(item) for item in items)
```
실체화된 리스트를 전달하지 마라 — 제너레이터 형태가 전체 리스트 할당을 피한다.

## 복잡한 반복에는 itertools 고려

알아야 할 핵심 함수들:
- `chain.from_iterable()` — 중첩된 이터러블 평탄화
- `islice()` — 모든 이터러블 슬라이싱 (시퀀스뿐 아니라)
- `groupby()` — 연속 요소 그룹화 (데이터가 사전 정렬되어 있어야 함)
- `product()`, `combinations()`, `permutations()` — 조합 순회
- `accumulate()` — 누적 합계 또는 커스텀 누적
- `batched()` (3.12+) — 이터러블을 고정 크기 그룹으로 분할

```python
from itertools import chain, batched

# 중첩 리스트 평탄화
flat = list(chain.from_iterable(nested))

# 청크 단위로 처리
for batch in batched(items, 100):
    process_batch(batch)
```

## 핵심 정리
- `enumerate` > `range(len(...))`, 병렬 순회에는 `zip(strict=True)`
- break가 있는 루프 패턴은 조기 반환하는 함수로 추출
- 누출된 루프 변수에 절대 의존하지 마라, 순회 중 절대 변경하지 마라
- 단락 검사에는 `any()`/`all()`과 제너레이터 사용
- 나머지는 `itertools` — 반복 바퀴를 재발명하지 마라
