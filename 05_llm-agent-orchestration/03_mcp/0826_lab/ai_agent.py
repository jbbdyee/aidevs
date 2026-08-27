"""GPT가 구조화된 MCP 결과로 개인화 습관 실험을 만드는 2단계 예제입니다.

실행 전 준비
    1. 과정 루트의 ``.env``에 ``OPENAI_API_KEY``와 ``OPENAI_MODEL``을 설정합니다.
    2. 가상환경에서 ``pip install -r requirements.txt``를 실행합니다.
    3. 이 파일만 실행합니다. ``mcp_server.py``는 직접 실행하지 않습니다.

실행 명령
    cd C:\\aidevs\\05_llm-agent-orchestration
    .\\.venv\\Scripts\\python.exe .\\03_mcp\\0826_lab\\ai_agent.py

전체 흐름
    사용자 ID와 자연어 요청
    → stdio MCP Client가 ``mcp_server.py``를 자식 프로세스로 자동 실행
    → MCP ``initialize``로 Client와 Server 기능 협상
    → MCP ``tools/list``로 프로필·기록·후보 행동 Tool Schema 발견
    → MCP Schema를 OpenAI Responses API의 Function Tool Schema로 변환
    → GPT가 요청을 이해하고 필요한 Tool 이름과 arguments 제안
    → Client가 Tool allowlist, user_id, arguments를 검증
    → MCP ``tools/call``로 Server의 구조화된 mock 데이터 조회
    → 모든 Tool Result를 ``function_call_output``과 ``call_id``로 GPT에 전달
    → 두 번째 GPT 호출이 목표·제약·기록·후보의 충돌을 조정
    → 개인화된 7일 습관 실험을 한국어로 반환
    → Client 종료 시 stdio MCP Server 자식 프로세스도 종료

역할과 권한 경계
    - GPT: 자연어 요청 이해, Tool 선택, 다기준 판단, 습관 실험 합성을 담당합니다.
    - MCP Client: Tool 발견, allowlist/user_id 검사, 호출, 결과 전달을 담당합니다.
    - MCP Server: 구조화된 데이터 조회와 arguments 검증을 담당합니다.
    - GPT는 Tool에 없는 건강 정보나 행동을 근거 없이 만들지 않습니다.

종료 조건과 안전장치
    - 첫 GPT 응답에 Function Call이 없으면 해당 응답으로 바로 종료합니다.
    - Server가 공개하지 않은 Tool 이름은 실행하지 않습니다.
    - arguments는 JSON Object이며 요청한 user_id와 같은지 확인합니다.
    - 모든 Tool Call, arguments, 결과, 오류 여부를 ``trace``에 기록합니다.

이 예제에서 Loop를 사용하지 않는 이유
    사용자 프로필, 최근 기록, 후보 행동은 서로의 결과에 의존하지 않습니다.
    GPT가 첫 응답에서 필요한 Tool을 모두 선택할 수 있으므로 병렬 조회 후 두 번째
    GPT 호출에서 최종 습관 실험을 합성하면 충분합니다.
"""

import asyncio
import json
import os
import sys
from pathlib import Path
from typing import Any, Literal

from dotenv import load_dotenv
from openai import AsyncOpenAI

from _stdio_client import connect_to_health_coach_server


UserId = Literal["demo_user", "busy_user"]
VALID_USER_IDS = {"demo_user", "busy_user"}

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
INSTRUCTIONS = """
당신은 개인화 건강 습관 실험 설계 Agent입니다.

기본 역할
- 사용자의 한국어 자연어 요청을 이해하고 필요한 MCP Tool을 선택하세요.
- 개인화된 7일 습관 실험 요청이면 get_health_profile,
  get_recent_habit_summary(days=7), get_habit_candidates를 모두 호출하세요.
- 프로필이나 최근 기록만 묻는 요청이면 필요한 Tool만 호출할 수 있습니다.
- Tool이 필요 없는 일반 개념 질문에는 Tool 없이 답할 수 있습니다.
- 필요한 Tool 결과를 받기 전에는 개인화된 최종 계획을 작성하지 마세요.

다기준 계획 판단
- Tool 결과는 이미 구조화되어 있으므로 키워드 추출이 아니라 목표, 제약,
  성공률, 실패 reason category, 성공한 context, 후보 행동을 함께 비교하세요.
- 우선순위는 안전 제한, 명시적 제약, 최근 실행 가능성, 사용자 선호,
  장기 목표 순서로 판단하세요.
- 한 번에 핵심 목표와 행동을 하나만 선택하세요.
- 같은 낮은 성공률이라도 late_work, forgot, too_difficult,
  schedule_changed 중 반복되는 이유에 따라 다른 해결 방식을 선택하세요.
- completion_rate는 전체 계획의 완료율이며 특정 category나 candidate의
  완료율이라고 표현하지 마세요.
- 선택한 행동, 최소 목표, 대체 행동은 get_habit_candidates 결과에 있는
  candidate와 fallback만 사용하세요.
- 선택한 candidate의 trigger, standard_minutes, minimum_minutes,
  recommended_frequency_per_week 값을 바꾸지 말고 그대로 사용하세요.
- max_session_minutes, allowed_intensity, available_slots를 넘지 마세요.
- Tool에 없는 사용자 상태나 의학적 사실을 만들지 마세요.
- 후보별 효과, 건강 개선 정도, 후보별 과거 성공률은 Tool에 제공되지 않으므로
  더 효과적이거나 성공률이 높다고 주장하지 마세요.
- 평균 수면·에너지 값은 숫자로만 기술하고 Tool에 기준값이 없으면
  부족하다, 낮다, 정상이다라고 판정하지 마세요.

최종 답변
- 내부 추론 전체를 노출하지 말고 Tool 결과로 확인 가능한 짧은 근거만 쓰세요.
- 아래 순서와 제목을 사용해 한국어로 작성하세요.
  [판단 근거]
  [이번 주 우선 목표]
  [7일 습관 실험]
  [회고 기준]
  [선택하지 않은 대안]
- 습관 실험에는 행동, 시작 신호, 일반 목표, 최소 목표, 대체 행동,
  주간 횟수를 포함하세요.
- 일반 목표에는 선택한 candidate의 standard_minutes를 정확히 쓰고,
  최소 목표에는 minimum_minutes를 정확히 쓰세요. 두 값을 섞지 마세요.
- 주간 횟수에는 recommended_frequency_per_week를 정확히 쓰세요.
- 최종 답변을 작성하기 전에 선택한 candidate의 숫자 세 값이 답변과
  일치하는지 확인하되, 확인 과정은 출력하지 마세요.
- 회고 기준은 실행 횟수, 시작하기 쉬웠는지, 같은 failure reason이
  반복됐는지만 사용하고 건강 효과를 추정하지 마세요.
- 회고 기준은 일주일 뒤 기록하거나 확인할 질문으로 작성하고, 아직 알 수 없는
  예/아니오나 성공 횟수를 미리 답하지 마세요.
- 선택하지 않은 대안 하나와 제외 이유를 Tool 결과에 근거해 설명하세요.
- 대안 제외 이유는 목표 priority, available_slots, constraints,
  failure_reason_counts, candidate 속성 중 실제 제공된 값만 사용하세요.
- [선택하지 않은 대안]에서는 후보를 설명할 때 성공률, 효과, 개선이라는
  단어를 사용하지 마세요.
- 이미 대체 행동으로 사용한 fallback_candidate_id는 [선택하지 않은 대안]에
  다시 쓰지 마세요. 선택한 행동 및 fallback과 다른 category의 후보 하나를
  고르고, 더 낮은 goal priority를 근거로 제외하세요.
- [선택하지 않은 대안]에는 goal priority 비교 이유 하나만 한 문장으로 쓰고
  시간, 횟수, 성공률, 효과에 관한 두 번째 이유를 덧붙이지 마세요.

건강·안전 경계
- 의료 진단, 치료, 복약 변경을 제안하지 마세요.
- 위험 신호가 명시되면 습관 실험보다 즉시 적절한 의료 도움 안내를 우선하세요.
- 이 프로그램은 일상 습관 코칭용이며 전문 의료 서비스를 대체하지 않습니다.
""".strip()


def to_openai_tool(tool) -> dict[str, Any]:
    """MCP Tool Schema를 OpenAI Responses API의 Function Tool로 변환합니다."""
    raw = tool.model_dump(by_alias=True)
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": raw["inputSchema"],
        "strict": False,
    }


def text_result(result) -> str:
    return "\n".join(
        content.text for content in result.content if hasattr(content, "text")
    )


async def answer(user_id: UserId, question: str) -> dict[str, Any]:
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY가 필요합니다.")
    if user_id not in VALID_USER_IDS:
        raise ValueError(f"지원하지 않는 user_id입니다: {user_id}")
    if not question.strip():
        raise ValueError("question은 빈 문자열일 수 없습니다.")

    trace: list[dict[str, Any]] = []
    agent_input = json.dumps(
        {"user_id": user_id, "request": question.strip()},
        ensure_ascii=False,
    )

    async with AsyncOpenAI() as client, connect_to_health_coach_server() as session:
        discovered = (await session.list_tools()).tools
        available = {tool.name for tool in discovered}
        openai_tools = [to_openai_tool(tool) for tool in discovered]
        response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            input=agent_input,
            tools=openai_tools,
            parallel_tool_calls=True,
        )

        tool_calls = [item for item in response.output if item.type == "function_call"]
        if not tool_calls:
            return {
                "question": question,
                "model": OPENAI_MODEL,
                "discovered_tools": sorted(available),
                "llm_calls": 1,
                "trace": trace,
                "answer": response.output_text,
            }

        tool_outputs = []
        for call in tool_calls:
            if call.name not in available:
                raise ValueError(f"MCP Server가 제공하지 않는 Tool입니다: {call.name}")

            arguments = json.loads(call.arguments)
            if not isinstance(arguments, dict):
                raise ValueError("Tool arguments는 JSON Object여야 합니다.")
            if arguments.get("user_id") != user_id:
                raise ValueError(
                    "Tool arguments의 user_id가 요청한 user_id와 일치하지 않습니다."
                )

            result = await session.call_tool(call.name, arguments)
            result_text = text_result(result)
            trace.append({
                "tool": call.name,
                "arguments": arguments,
                "is_error": bool(result.isError),
                "result": result_text,
            })
            tool_outputs.append({
                "type": "function_call_output",
                "call_id": call.call_id,
                "output": result_text,
            })

        final_response = await client.responses.create(
            model=OPENAI_MODEL,
            instructions=INSTRUCTIONS,
            previous_response_id=response.id,
            input=tool_outputs,
        )
        return {
            "question": question,
            "model": OPENAI_MODEL,
            "discovered_tools": sorted(available),
            "llm_calls": 2,
            "trace": trace,
            "answer": final_response.output_text,
        }


async def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # result = await answer("demo_user", "최근 7일 습관 기록을 요약해 주세요.")
    # result = await answer("busy_user", "실행 가능한 7일 습관을 설계해 주세요.")
    result = await answer(
        "demo_user",
        "현재 목표와 최근 기록을 바탕으로 이번 주 습관 실험을 설계해 주세요.",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
