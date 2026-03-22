# 2장: 문자열과 슬라이싱 (항목 10–16)

## 슬라이싱 기본 원칙

### 슬라이싱은 단순하고 읽기 쉽게
```python
# 좋음: 의도가 명확
first_five = items[:5]
last_three = items[-3:]
every_other = items[::2]

# 나쁨: 시작, 끝, 스트라이드를 동시에 사용하지 마라
confusing = items[2:10:3]  # 머릿속으로 계산하기 어려움

# 더 나음: 두 단계로 분리
subset = items[2:10]
result = subset[::3]
```

### 시작/끝과 함께 음수 스트라이드 사용 피하기
`items[-2::-2]`는 인지적 퍼즐이다. 두 단계 연산으로 분리하라.
역방향 순회만 필요할 때는 `reversed()`를 선호하라.

### 슬라이싱은 복사를 생성하고, 대입은 변경함
```python
b = a[:]       # 얕은 복사
a[2:5] = [10]  # `a`를 제자리에서 변경 — 길이가 바뀔 수 있다!
```

### 스타 표현식으로 나머지 수집 언패킹
```python
# 머리/꼬리 패턴을 깔끔하게 추출
first, *rest = items
*init, last = items
head, *_, tail = items  # 중간 요소 무시
```
스타 언패킹은 비어 있어도 항상 `list`를 생성한다.
수동 인덱싱과 경계값 오류(off-by-one)를 피하기 위해 사용하라.

## 문자열 전용 패턴

### `str.removeprefix()` / `str.removesuffix()` 선호 (3.9+)
```python
# 나쁨: 매직 넘버를 사용한 수동 슬라이싱
if s.startswith("test_"):
    name = s[5:]

# 좋음: 자기 설명적
name = s.removeprefix("test_")
```

### 멀티라인 문자열
깔끔한 멀티라인 내용을 위해 삼중 따옴표 문자열과 `textwrap.dedent()`를 사용하라:
```python
import textwrap
query = textwrap.dedent("""\
    SELECT *
    FROM users
    WHERE active = true
""")
```

## 핵심 정리
- 슬라이스에는 (시작, 끝, 스트라이드) 중 최대 두 가지만 동시에 사용
- 가변 길이 시퀀스에는 스타 언패킹 사용
- 수동 슬라이싱 대신 `removeprefix`/`removesuffix` 선호
- 깔끔한 멀티라인 문자열에는 `textwrap.dedent`
