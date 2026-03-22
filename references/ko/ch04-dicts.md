# 4장: 딕셔너리 (항목 25–29)

## 딕셔너리 삽입 순서

Python 3.7부터 dict는 삽입 순서를 보존한다. 이에 의존할 수 있지만, 주의하라:
- 외부 소스(JSON, DB 결과)의 dict가 특정 순서를 갖는다고 가정하지 마라
- 순서가 의미적으로 중요하다면, `OrderedDict`가 의도를 더 명확히 하는지 고려하라
- 키워드 인자(`**kwargs`)도 순서를 보존한다

## 누락된 키 처리

### in + KeyError보다 get() 선호
```python
# 나쁨: 두 번 조회
if key in d:
    value = d[key]
else:
    value = default

# 나쁨: LBYL + 예외 처리 혼합
try:
    value = d[key]
except KeyError:
    value = default

# 좋음: 한 번 조회
value = d.get(key, default)
```

### setdefault는 절제하여 사용
`setdefault`는 기본값을 삽입하고 동시에 참조를 얻을 때 유용하지만,
코드가 읽기 어렵다. 이 패턴에는 `defaultdict`를 선호하라:
```python
# 일회성인 경우 허용 가능
d.setdefault(key, []).append(item)

# 반복 사용에는 더 나음: defaultdict
from collections import defaultdict
d = defaultdict(list)
d[key].append(item)
```

### 내부 상태에는 defaultdict
내부 집계를 구축할 때 `defaultdict`를 사용하라:
```python
from collections import defaultdict

# 그룹화
groups = defaultdict(list)
for item in items:
    groups[item.category].append(item)

# 카운팅 (Counter가 이 경우에는 더 좋지만)
counts = defaultdict(int)
for word in words:
    counts[word] += 1

# 카운팅에는 이게 더 나음:
from collections import Counter
counts = Counter(words)
```

### 키에 의존하는 기본값에는 __missing__
기본값이 키 자체에 의존하는 경우, `defaultdict`로는 부족하다.
`dict`를 상속하고 `__missing__`을 구현하라:
```python
class PictureCache(dict):
    def __missing__(self, key: str) -> bytes:
        value = load_picture(key)
        self[key] = value
        return value

cache = PictureCache()
image = cache["photo.jpg"]  # 첫 접근 시 로드, 이후 캐시됨
```
이것은 지연 로딩 캐시와 설정 조회에 깔끔한 패턴이다.

## 중첩 대신 클래스로 구성

딕셔너리를 2레벨 이상 중첩하고 있다면, 클래스를 만들 때다:
```python
# 나쁨: 깊이 중첩된 딕셔너리
students["Alice"]["grades"]["math"].append(95)

# 좋음: 데이터클래스로 구성
@dataclass
class Student:
    name: str
    grades: dict[str, list[int]] = field(default_factory=dict)

    def add_grade(self, subject: str, score: int) -> None:
        self.grades.setdefault(subject, []).append(score)
```

## 핵심 정리
- 안전한 조회에는 `dict.get(key, default)`
- 그룹화/카운팅 패턴에는 `defaultdict`
- 키 의존 기본값 계산에는 `__missing__`
- 딕셔너리를 2레벨 이상 중첩할 때는 클래스로 리팩토링
- 빈도 카운팅에는 `Counter`
