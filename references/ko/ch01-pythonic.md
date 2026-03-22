# 1장: 파이썬다운 사고 (항목 1–16)

핵심 철학: 파이썬 언어의 고유한 강점을 활용하는 코드를 작성하라.
파이썬에는 대부분의 작업에 대한 "정석(canonical)" 방식이 있다 — 이를 배우고 따르라.

## 버전과 스타일 기초

- 항상 Python 버전을 파악하라 (`python3 --version`). 최신 기능을 위해 3.10+ 대상.
- PEP 8을 철저히 따르라: 4칸 들여쓰기, 함수/변수에는 snake_case,
  클래스에는 PascalCase, 모듈 레벨 상수에는 UPPER_CASE.
- 포매터(black, ruff format)를 사용하여 스타일 논쟁을 없애라.
- 파이썬은 동적 타입 언어이다 — 컴파일 타임 안전성을 기대하지 마라. 타입 힌트 +
  mypy/pyright를 "컴파일러"로 사용하라.

## 표현식과 대입

### 복잡한 표현식보다 도우미 함수
```python
# 나쁨: 밀도가 높고, 디버그하기 어려움
result = (value if value > 0 else 0) * rate if rate else default

# 좋음: 이름이 있는 중간 단계
clamped = max(value, 0)
result = clamped * rate if rate else default
```

표현식이 삼항 연산자를 중첩하거나 여러 불리언 조건을 결합할 때,
도우미 함수로 추출하라. 함수 이름이 의도를 문서화한다.

### 인덱싱보다 언패킹
```python
# 나쁨: 위치 기반 인덱싱은 깨지기 쉽고 불명확
name = record[0]
age = record[1]

# 좋음: 언패킹은 구조를 전달
name, age = record

# 좋음: 가변 길이 시퀀스에 대한 스타 언패킹
first, *middle, last = scores
```

### 단일 요소 튜플 안전
단일 요소 튜플은 항상 괄호로 감싸서 잠재적 버그를 방지하라:
```python
values = (1,)  # 튜플 — 명확
values = 1,    # 이것도 튜플이지만, 쉼표를 놓치기 쉬움
```

### 조건부 표현식
인라인 `if`/`else`는 결과가 단순하고 읽기 쉬울 때만 사용하라.
어느 쪽 분기에 부수 효과가 있거나 복잡하다면, 전체 `if` 블록을 사용하라.

### 왈러스 연산자 (:=)
대입 표현식을 사용하여 중복 호출을 피하라, 특히 `while` 루프와
컴프리헨션 필터에서:
```python
# 좋음: 한 번 계산, 두 번 사용
if (n := len(data)) > 10:
    print(f"{n}개 항목 처리 중")

# 좋음: 컴프리헨션 필터에서
results = [y for x in data if (y := transform(x)) is not None]
```
가독성을 해치는 곳에서는 왈러스를 피하라. 이미 복잡한 줄이라면,
별도의 대입을 사용하라.

### match/case로 구조 분해
알려진 형태의 데이터(JSON 응답, 커맨드 객체, AST 노드)를 구조 분해할 때
`match`/`case`를 사용하라. 스칼라 값에 대한 단순한 `if`/`elif` 체인의
대체로 사용하지 마라 — 그것은 match/case의 강점이 아니다.
```python
# 좋음: 구조적 매칭
match command:
    case {"action": "move", "direction": str(d)}:
        move(d)
    case {"action": "quit"}:
        shutdown()
    case _:
        raise ValueError(f"알 수 없는 커맨드: {command}")
```

## 문자열과 포매팅

### format()과 % 대신 f-string
f-string이 가장 읽기 쉽고 빠른 문자열 보간 방법이다.
지연 포매팅(로깅, 국제화)이 필요하지 않다면 f-string을 사용하라.
```python
# 좋음
print(f"안녕하세요, {name}님! {count:,}개의 항목이 있습니다.")

# 지연 포매팅이 필요한 경우
logger.info("Processing %s items", count)  # 로깅에서는 f-string 피하기
```

### 디버깅을 위한 f-string의 repr()
타입을 구분하기 위해 디버그 출력에 `!r`을 사용하라:
```python
print(f"값: {x!r}")  # 문자열 주위에 따옴표를 표시, None과 "None"을 구분
```

## 바이트 vs 문자열

- 텍스트(유니코드)에는 `str`, 바이너리 데이터에는 `bytes`. 절대 섞지 마라.
- I/O 경계에서만 인코딩/디코딩하라, 명시적 인코딩 사용(utf-8 선호).
- 경계에서 작업할 때 인코딩/디코딩용 도우미 함수를 작성하라.

## 핵심 정리
- 복잡한 것은 잘 명명된 도우미 함수로 추출하라
- 언패킹, 왈러스, match/case로 노이즈를 줄이되 — 명확성을 희생하지 마라
- 포매팅에는 f-string, 경계에서는 명시적 인코딩
- 기계적 스타일은 도구(포매터, 타입 체커)에게 맡기라
