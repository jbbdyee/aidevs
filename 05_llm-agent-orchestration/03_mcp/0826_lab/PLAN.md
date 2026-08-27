# 개인화 건강 습관 코치 AI Agent 구현 계획

## 1. 목표

현재 예제의 `ai_agent.py` + `_stdio_client.py` + `mcp_server.py` 구조와 2단계 MCP Tool Calling 방식을 그대로 유지하면서, **구조화된 사용자 조건과 최근 기록 사이의 충돌을 조정하여 개인화된 습관 실험을 합성하는 AI Agent**를 만든다.

LLM이 필요한 이유를 자연어 이해 능력으로 설명하지 않는다. MCP Tool은 사용자 정보를 이미 구조화된 값으로 반환하고, LLM은 그 결과를 근거로 여러 목표·제약·실패 패턴·후보 행동 사이의 우선순위를 정하고 하나의 새로운 습관 실험으로 조합한다.

이 프로그램은 의료 진단이나 치료를 제공하지 않는다. 수면, 가벼운 활동, 수분, 회복 등 일상 건강 습관을 설계하는 교육용 예제로 한정한다.

## 2. 현재 예제 구조를 그대로 유지하는 원칙

새 폴더, 데이터베이스, 스케줄러, 웹 UI, CLI 시나리오 시스템을 추가하지 않는다.

```text
0826_lab/
├─ ai_agent.py       # LLM Tool 선택, 결과 종합, 최종 습관 실험 생성
├─ _stdio_client.py  # stdio MCP Server 연결
├─ mcp_server.py     # 구조화된 건강 정보 Tool 3개
└─ PLAN.md           # 구현 계획
```

유지할 코드 형식:

- `FastMCP`로 Tool을 공개한다.
- `AsyncOpenAI`와 Responses API를 사용한다.
- `_stdio_client.py`가 `mcp_server.py`를 자식 프로세스로 실행한다.
- `tools/list`로 Tool Schema를 발견한다.
- `to_openai_tool()`로 MCP Schema를 OpenAI Function Tool Schema로 변환한다.
- 첫 번째 LLM 호출에서 필요한 Tool을 선택한다.
- Tool은 서로 독립적으로 호출할 수 있게 설계하고 `parallel_tool_calls=True`를 유지한다.
- 모든 Tool 결과를 모아 두 번째 LLM 호출에 전달한다.
- 두 번째 LLM 호출은 Tool 없이 개인화된 습관 실험을 생성한다.
- `question`, `model`, `discovered_tools`, `llm_calls`, `trace`, `answer` 반환 구조를 유지한다.
- `main()`에서 예제 질문 하나를 실행하고 다른 예제는 주석으로 전환할 수 있게 한다.

## 3. LLM이 반드시 필요한 Agent 기능

Agent의 핵심 기능은 **다기준 제약 조정 기반 습관 실험 합성(Multi-constraint Habit Experiment Synthesis)**이다.

### 3.1 여러 목표 사이의 우선순위 결정

사용자에게 수면 개선, 체력 향상, 수분 섭취처럼 여러 목표가 있을 때 모든 목표를 동시에 추천하지 않는다. 최근 상태, 가용 시간, 반복 실패 패턴, 선호를 함께 보고 이번 주에 먼저 다룰 목표 하나를 선택한다.

단순 점수 합산이 아니라 다음처럼 서로 다른 종류의 조건을 함께 판단한다.

- 목표의 중요도
- 현재 부족한 상태
- 실행 가능한 시간대와 시간 길이
- 최근 성공률
- 반복된 실패 유형
- 선호하거나 피하고 싶은 행동
- 후보 행동이 가진 난이도와 적용 조건

### 3.2 충돌하는 조건 사이의 절충안 생성

예를 들어 사용자가 체력 향상을 원하지만 최근 퇴근 후 활동을 반복해서 실패했고 점심시간에는 10분만 사용할 수 있다면, “운동을 더 열심히 한다” 또는 “운동을 포기한다” 중 하나를 고르지 않는다.

LLM은 후보 행동의 구성 요소를 조합해 “점심 식사 후 7분 걷기, 바쁜 날에는 2분 걷기, 주 3회”와 같은 절충안을 만든다.

### 3.3 같은 결과에서 서로 다른 원인 가설 비교

성공률이 똑같이 20%여도 실패 원인이 시간 부족, 너무 높은 난이도, 시작 신호 부재, 선호 불일치라면 다른 계획이 필요하다.

MCP Tool은 실패 원인을 이미 구조화된 category와 횟수로 반환한다. LLM은 자연어를 해석하는 것이 아니라 여러 가능한 설명 중 현재 기록을 가장 잘 설명하는 행동적 장애물 가설을 선택한다.

### 3.4 후보 행동을 새로운 실험으로 구성

Tool은 완성된 추천 문장을 반환하지 않고 안전한 행동 블록만 제공한다.

예:

- 점심 후 걷기
- 취침 준비 알람
- 물병을 책상에 놓기
- 2분 최소 행동
- 실내 대체 행동

LLM은 프로필과 최근 기록을 근거로 적절한 블록을 선택하고 다음 요소를 갖춘 하나의 습관 실험으로 합성한다.

- 이번 주 우선 목표
- 선택한 행동
- 시작 신호
- 일반 목표
- 힘든 날의 최소 목표
- 실패 조건을 고려한 대체 행동
- 주간 실행 횟수
- 일주일 후 회고 기준

### 3.5 선택하지 않은 대안과의 트레이드오프 설명

Agent는 단순 추천 목록을 출력하지 않는다. 왜 특정 행동을 선택했는지, 더 강한 행동이나 다른 시간대를 선택하지 않은 이유를 Tool 결과에 근거해 짧게 설명한다.

이 기능은 추천 결과의 검증 가능성을 높이고, 고정된 “성공률이 낮으면 강도를 낮춘다” 규칙과 구분된다.

## 4. LLM 기능으로 주장하지 않을 부분

다음 기능은 일반 코드나 MCP Tool이 담당하며, Agent가 필요한 근거로 사용하지 않는다.

- 사용자 질문에서 키워드를 추출하는 자연어 이해
- 숫자 범위 검증
- 평균과 성공률 계산
- 실패 이유별 횟수 집계
- 사용자 정보 조회
- 후보 습관 목록 조회
- Tool allowlist 검사
- JSON arguments 검증
- 고정된 안전 제한

즉, **입력 이해가 아니라 구조화된 근거를 이용한 우선순위 판단, 조건 충돌 해결, 새로운 계획 합성**이 LLM의 핵심 역할이다.

## 5. Agent 역할과 출력 계약

Agent의 역할은 **개인화 건강 습관 실험 설계자**이다.

개인화 계획 요청을 받으면 다음 원칙으로 판단한다.

1. 안전 제한을 위반하는 후보는 제외한다.
2. 사용자의 명시적 제약을 우선한다.
3. 최근 반복 실패와 관련된 조건을 피하거나 수정한다.
4. 사용 가능한 시간 안에서 실행 가능한 행동을 선택한다.
5. 사용자의 선호와 장기 목표를 반영한다.
6. 한 번에 핵심 습관 하나만 선택한다.
7. 근거 없는 건강 정보나 Tool에 없는 후보를 만들지 않는다.

최종 답변 형식:

```text
[판단 근거]
- 프로필과 최근 기록에서 확인한 핵심 사실

[이번 주 우선 목표]
- 선택한 목표와 선택 이유

[7일 습관 실험]
- 행동
- 시작 신호
- 일반 목표
- 최소 목표
- 대체 행동
- 주간 횟수

[회고 기준]
- 일주일 뒤 확인할 항목

[선택하지 않은 대안]
- 제외한 대안과 짧은 이유
```

## 6. MCP Tool 설계: 총 3개

세 Tool은 모두 조회 전용이며 서로의 결과에 의존하지 않는다. 따라서 현재 여행 예제처럼 첫 번째 LLM 응답에서 모두 선택하고 병렬로 실행할 수 있다.

### Tool 1. `get_health_profile`

사용자의 장기 목표, 생활 제약, 선호, 안전 제한을 구조화된 형태로 제공한다.

입력:

- `user_id: Literal["demo_user", "busy_user"]`

출력 예:

```json
{
  "user_id": "demo_user",
  "goals": [
    {"category": "activity", "priority": 1},
    {"category": "sleep", "priority": 2}
  ],
  "available_slots": [
    {"slot": "lunch", "minutes": 10}
  ],
  "preferences": {
    "avoid_time": "morning",
    "preferred_location": "outdoor"
  },
  "constraints": {
    "max_session_minutes": 10,
    "allowed_intensity": "light"
  },
  "source": "demo-health-profile"
}
```

Tool 책임:

- 저장된 구조화 정보를 그대로 반환한다.
- 어떤 목표를 우선할지 결정하지 않는다.
- 최종 습관 계획을 추천하지 않는다.

### Tool 2. `get_recent_habit_summary`

최근 습관 기록을 계산 가능한 통계와 category로 요약한다.

입력:

- `user_id: Literal["demo_user", "busy_user"]`
- `days: int = 7`

출력 예:

```json
{
  "period_days": 7,
  "completion_rate": 0.2,
  "average_sleep_hours": 6.1,
  "average_energy_level": 2.8,
  "failure_reason_counts": {
    "late_work": 3,
    "forgot": 1,
    "too_difficult": 0
  },
  "successful_contexts": ["lunch"],
  "source": "demo-habit-history"
}
```

Tool 책임:

- `days`를 1~30 범위로 검증한다.
- 성공률, 평균, 실패 category 횟수를 반환한다.
- 실패 원인을 해석하거나 새 계획을 만들지 않는다.

### Tool 3. `get_habit_candidates`

사용자에게 적용할 수 있는 안전한 습관 행동 블록을 제공한다.

입력:

- `user_id: Literal["demo_user", "busy_user"]`

출력 예:

```json
{
  "items": [
    {
      "candidate_id": "walk_after_lunch",
      "category": "activity",
      "trigger": "after_lunch",
      "standard_minutes": 7,
      "minimum_minutes": 2,
      "recommended_frequency_per_week": 3,
      "allowed_slots": ["lunch"],
      "intensity": "light",
      "fallback": "indoor_walk"
    },
    {
      "candidate_id": "bedtime_wind_down",
      "category": "sleep",
      "trigger": "bedtime_alarm",
      "standard_minutes": 10,
      "minimum_minutes": 3,
      "allowed_slots": ["night"],
      "intensity": "light",
      "fallback": "dim_lights"
    }
  ],
  "source": "demo-habit-catalog"
}
```

Tool 책임:

- 안전 검토된 후보 행동과 허용 범위를 반환한다.
- 후보의 순위를 정하거나 최종 행동을 선택하지 않는다.
- LLM이 Tool에 없는 새로운 건강 행동을 임의로 만들지 못하게 근거를 제공한다.

## 7. 현재 예제와 동일한 2단계 실행 흐름

`ai_agent.py`의 `answer(user_id, question)`은 다음처럼 동작한다.

```text
사용자 ID + 요청
  ↓
stdio MCP Client가 mcp_server.py 실행
  ↓
initialize와 tools/list
  ↓
MCP Schema를 OpenAI Function Tool Schema로 변환
  ↓
첫 번째 LLM 호출
  ↓
필요한 Tool 이름과 arguments 선택
  ↓
Client allowlist와 JSON Object 검증
  ↓
MCP tools/call 실행
  ↓
모든 Tool Result를 function_call_output으로 전달
  ↓
두 번째 LLM 호출
  ↓
구조화된 결과를 종합해 7일 습관 실험 생성
  ↓
JSON trace와 최종 답변 출력
```

현재 예제처럼 반복 Agent Loop를 추가하지 않는다. 세 조회 Tool은 서로 독립적이고, 두 번째 LLM 호출에서 필요한 모든 근거가 모이기 때문이다.

종료 조건과 안전장치:

- 개인화 계획 요청이면 세 Tool을 모두 호출하도록 `INSTRUCTIONS`에 명시한다.
- 프로필 또는 최근 기록만 묻는 요청이면 필요한 Tool만 호출할 수 있다.
- Tool이 필요 없는 일반 질문이면 첫 번째 LLM 응답으로 종료한다.
- 서버가 공개하지 않은 Tool 이름은 실행하지 않는다.
- arguments가 JSON Object인지 확인한다.
- 모든 Tool 이름, arguments, 결과, 오류 여부를 `trace`에 기록한다.
- 두 번째 LLM 호출에는 Tool을 다시 제공하지 않아 추가 호출을 막는다.

## 8. 파일별 변경 계획

### `mcp_server.py`

- 여행용 서버 이름을 건강 습관 코치용으로 변경한다.
- 날씨·호텔 Tool과 여행 resource를 제거한다.
- `get_health_profile`, `get_recent_habit_summary`, `get_habit_candidates`를 구현한다.
- 현재 예제처럼 함수 내부의 교육용 mock dict/list 데이터를 반환한다.
- SQLite나 별도 데이터 파일을 추가하지 않는다.
- 입력값 검증과 `source` 필드를 유지한다.

### `_stdio_client.py`

- 존재하지 않는 `22mcp_server.py` 경로를 실제 `mcp_server.py`로 수정한다.
- `connect_to_travel_server()`를 `connect_to_health_coach_server()`로 변경한다.
- `StdioServerParameters`, `stdio_client`, `ClientSession`, `initialize()` 구조는 그대로 유지한다.

### `ai_agent.py`

- 여행 설명과 `INSTRUCTIONS`를 개인화 습관 실험 설계 Agent로 변경한다.
- `answer(question)`을 `answer(user_id, question)`으로만 최소 변경한다.
- 현재의 `to_openai_tool()`, `text_result()`, Tool allowlist, JSON 검증 코드를 유지한다.
- 현재처럼 첫 LLM 호출 → Tool 실행 → 두 번째 LLM 호출 구조를 유지한다.
- `parallel_tool_calls=True`를 유지한다.
- 최종 반환 JSON 필드를 그대로 유지한다.
- `main()`의 예제 질문만 건강 습관 코칭 시나리오로 변경한다.

## 9. 실행했을 때 보이는 예제

`main()`은 현재 예제처럼 여러 질문을 주석으로 두고 하나만 활성화한다.

```python
async def main() -> None:
    # result = await answer("demo_user", "최근 기록을 요약해 주세요.")
    # result = await answer("busy_user", "실행 가능한 7일 습관을 설계해 주세요.")
    result = await answer(
        "demo_user",
        "현재 목표와 최근 기록을 바탕으로 이번 주 습관 실험을 설계해 주세요.",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
```

예상 trace:

```json
{
  "question": "현재 목표와 최근 기록을 바탕으로 이번 주 습관 실험을 설계해 주세요.",
  "model": "configured-model",
  "discovered_tools": [
    "get_habit_candidates",
    "get_health_profile",
    "get_recent_habit_summary"
  ],
  "llm_calls": 2,
  "trace": [
    {
      "tool": "get_health_profile",
      "arguments": {"user_id": "demo_user"},
      "is_error": false
    },
    {
      "tool": "get_recent_habit_summary",
      "arguments": {"user_id": "demo_user", "days": 7},
      "is_error": false
    },
    {
      "tool": "get_habit_candidates",
      "arguments": {"user_id": "demo_user"},
      "is_error": false
    }
  ],
  "answer": "프로필과 최근 기록을 종합한 7일 습관 실험..."
}
```

예상 최종 답변:

```text
[판단 근거]
- 활동이 1순위 목표지만 퇴근 후 계획의 최근 성공률은 20%입니다.
- 실패 4회 중 3회가 야근과 관련되어 있습니다.
- 점심시간에는 10분을 사용할 수 있고, 점심 실행 기록은 성공한 적이 있습니다.

[이번 주 우선 목표]
- 활동 습관의 실행 시점을 퇴근 후에서 점심시간으로 변경합니다.

[7일 습관 실험]
- 행동: 점심 식사 후 가볍게 걷기
- 시작 신호: 점심 식사를 마친 직후
- 일반 목표: 7분
- 최소 목표: 바쁜 날에는 2분
- 대체 행동: 밖에 나가기 어려우면 실내 복도 걷기
- 횟수: 주 3회

[회고 기준]
- 3회 중 실제로 시작한 횟수와 점심시간이 실행하기 쉬웠는지 확인합니다.

[선택하지 않은 대안]
- 퇴근 후 20분 걷기는 야근과 반복해서 충돌했기 때문에 이번 실험에서 제외했습니다.
```

이 출력에서 LLM의 핵심 기능은 질문 해석이 아니라 **세 Tool의 구조화된 결과를 함께 비교하여 시간대, 행동, 최소 목표, 대체 행동을 하나의 일관된 실험으로 구성한 것**이다.

## 10. 건강·안전 경계

- 질병을 진단하지 않는다.
- 약 시작·중단·증량을 제안하지 않는다.
- 극단적인 식사 제한이나 고강도 행동을 만들지 않는다.
- Tool이 제공하지 않은 건강 행동을 임의로 추가하지 않는다.
- 프로필의 `allowed_intensity`와 `max_session_minutes`를 넘지 않는다.
- 위험 신호가 포함된 mock profile은 일반 계획 대신 전문적인 도움 안내를 반환하도록 `INSTRUCTIONS`에 명시한다.
- 서버에서도 시간, 강도, 허용 category를 결정론적으로 제한한다.

## 11. 검증 계획

### 구조 회귀 검증

- Python 파일 3개 중심의 평면 구조가 유지되는지 확인한다.
- MCP Server가 정확히 3개 Tool만 공개하는지 확인한다.
- stdio initialize → tools/list → tools/call 흐름이 유지되는지 확인한다.
- 첫 번째 LLM 호출과 두 번째 LLM 호출의 최대 2회 구조가 유지되는지 확인한다.
- `parallel_tool_calls=True`와 기존 trace 형식이 유지되는지 확인한다.
- 별도 DB, 스케줄러, 웹 UI가 추가되지 않았는지 확인한다.

### Tool 검증

- `demo_user`와 `busy_user` 프로필이 서로 다른 구조화 결과를 반환하는지 확인한다.
- `days`가 1~30 범위를 벗어나면 서버가 거부하는지 확인한다.
- 후보 Tool이 완성된 추천이 아니라 행동 블록만 반환하는지 확인한다.
- 모든 Tool Result에 `source`가 포함되는지 확인한다.

### LLM Agent 기능 검증

- 같은 목표라도 프로필과 실패 category가 다르면 서로 다른 습관 실험을 생성하는지 확인한다.
- 목표 우선순위와 최근 실행 가능성이 충돌할 때 하나를 선택하고 근거를 설명하는지 확인한다.
- 선택한 행동이 후보 Tool의 `candidate_id`와 허용 범위에 근거하는지 확인한다.
- 최종 실험에 시작 신호, 일반 목표, 최소 목표, 대체 행동, 횟수, 회고 기준이 포함되는지 확인한다.
- 선택하지 않은 대안과 트레이드오프를 Tool 결과에 근거해 설명하는지 확인한다.
- Tool에 없는 건강 정보나 행동을 만들지 않는지 확인한다.
- 내부 chain-of-thought가 아니라 짧은 판단 근거만 출력하는지 확인한다.

정확한 문장 일치로 평가하지 않고, 필수 요소와 근거 일치 여부를 평가한다.

## 12. 구현 순서

1. 여행 도메인 이름과 잘못된 Server 경로를 건강 습관 코치 기준으로 변경한다.
2. `mcp_server.py`의 여행 Tool을 구조화된 건강 Tool 3개로 교체한다.
3. 각 Tool의 mock 데이터, 입력 검증, Schema를 직접 확인한다.
4. `ai_agent.py`의 `INSTRUCTIONS`와 예제 질문을 변경한다.
5. 기존 2단계 Tool Calling 흐름으로 세 Tool 결과를 종합하게 한다.
6. JSON trace와 최종 습관 실험 출력 형식을 검증한다.
7. `demo_user`와 `busy_user` 결과가 조건에 맞게 달라지는지 확인한다.

## 13. 완료 조건

- 현재 폴더와 3개 Python 파일 구조가 유지된다.
- 기존 stdio MCP 연결과 2단계 Tool Calling 코드 형식이 유지된다.
- Tool은 `get_health_profile`, `get_recent_habit_summary`, `get_habit_candidates` 3개만 제공된다.
- Tool 결과는 자연어 해석이 필요 없는 구조화된 데이터이다.
- LLM은 여러 목표·제약·기록·후보 사이의 우선순위를 결정한다.
- LLM은 후보 행동 블록을 하나의 새로운 7일 습관 실험으로 합성한다.
- 최종 답변이 선택 근거와 제외한 대안의 트레이드오프를 포함한다.
- 실행 결과에 기존 형식의 `llm_calls`와 전체 Tool `trace`가 남는다.
- SQLite, 스케줄러, 권한 시스템, 대화형 CLI 같은 추가 구조가 없다.
