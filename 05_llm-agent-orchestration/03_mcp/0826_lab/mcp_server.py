"""구조화된 개인화 데이터를 제공하는 교육용 건강 습관 MCP Server입니다."""

from collections import Counter
from copy import deepcopy
from statistics import mean
from typing import Literal

from mcp.server.fastmcp import FastMCP


UserId = Literal["demo_user", "busy_user"]

mcp = FastMCP(
    "health-habit-tools",
    instructions=(
        "사용자 프로필, 최근 습관 요약, 안전한 습관 후보를 구조화된 "
        "데이터로 제공하는 교육용 MCP Server입니다."
    ),
)

_PROFILES = {
    "demo_user": {
        "goals": [
            {"category": "activity", "priority": 1},
            {"category": "sleep", "priority": 2},
        ],
        "available_slots": [
            {"slot": "lunch", "minutes": 10},
            {"slot": "evening", "minutes": 15},
        ],
        "preferences": {
            "avoid_time": "morning",
            "preferred_location": "outdoor",
            "coaching_style": "single_clear_plan",
        },
        "constraints": {
            "max_session_minutes": 10,
            "allowed_intensity": "light",
            "excluded_actions": ["high_impact", "fasted_workout"],
        },
        "safety": {"red_flags_present": False},
    },
    "busy_user": {
        "goals": [
            {"category": "sleep", "priority": 1},
            {"category": "recovery", "priority": 2},
            {"category": "hydration", "priority": 3},
        ],
        "available_slots": [
            {"slot": "afternoon", "minutes": 5},
            {"slot": "night", "minutes": 10},
        ],
        "preferences": {
            "avoid_time": "morning",
            "preferred_location": "indoor",
            "coaching_style": "minimal_steps",
        },
        "constraints": {
            "max_session_minutes": 10,
            "allowed_intensity": "light",
            "schedule_pattern": "irregular",
            "excluded_actions": ["high_impact", "strict_meal_restriction"],
        },
        "safety": {"red_flags_present": False},
    },
}

_HISTORY = {
    "demo_user": [
        {
            "day_offset": -6,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.8,
            "energy_level": 2,
            "failure_reason": "late_work",
            "context": "evening",
        },
        {
            "day_offset": -5,
            "planned": True,
            "completed": True,
            "sleep_hours": 6.5,
            "energy_level": 3,
            "failure_reason": None,
            "context": "lunch",
        },
        {
            "day_offset": -4,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.9,
            "energy_level": 2,
            "failure_reason": "late_work",
            "context": "evening",
        },
        {
            "day_offset": -3,
            "planned": False,
            "completed": False,
            "sleep_hours": 6.4,
            "energy_level": 3,
            "failure_reason": None,
            "context": None,
        },
        {
            "day_offset": -2,
            "planned": True,
            "completed": False,
            "sleep_hours": 6.1,
            "energy_level": 3,
            "failure_reason": "forgot",
            "context": "evening",
        },
        {
            "day_offset": -1,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.7,
            "energy_level": 2,
            "failure_reason": "late_work",
            "context": "evening",
        },
        {
            "day_offset": 0,
            "planned": False,
            "completed": False,
            "sleep_hours": 6.3,
            "energy_level": 3,
            "failure_reason": None,
            "context": None,
        },
    ],
    "busy_user": [
        {
            "day_offset": -6,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.2,
            "energy_level": 2,
            "failure_reason": "schedule_changed",
            "context": "night",
        },
        {
            "day_offset": -5,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.5,
            "energy_level": 2,
            "failure_reason": "too_difficult",
            "context": "night",
        },
        {
            "day_offset": -4,
            "planned": False,
            "completed": False,
            "sleep_hours": 6.0,
            "energy_level": 3,
            "failure_reason": None,
            "context": None,
        },
        {
            "day_offset": -3,
            "planned": True,
            "completed": True,
            "sleep_hours": 6.2,
            "energy_level": 3,
            "failure_reason": None,
            "context": "night",
        },
        {
            "day_offset": -2,
            "planned": True,
            "completed": False,
            "sleep_hours": 5.4,
            "energy_level": 2,
            "failure_reason": "schedule_changed",
            "context": "night",
        },
        {
            "day_offset": -1,
            "planned": False,
            "completed": False,
            "sleep_hours": 5.8,
            "energy_level": 2,
            "failure_reason": None,
            "context": None,
        },
        {
            "day_offset": 0,
            "planned": False,
            "completed": False,
            "sleep_hours": 5.6,
            "energy_level": 2,
            "failure_reason": None,
            "context": None,
        },
    ],
}

_CANDIDATES = {
    "demo_user": [
        {
            "candidate_id": "walk_after_lunch",
            "category": "activity",
            "trigger": "after_lunch",
            "standard_minutes": 7,
            "minimum_minutes": 2,
            "recommended_frequency_per_week": 3,
            "allowed_slots": ["lunch"],
            "intensity": "light",
            "fallback_candidate_id": "indoor_walk",
        },
        {
            "candidate_id": "indoor_walk",
            "category": "activity",
            "trigger": "after_lunch",
            "standard_minutes": 5,
            "minimum_minutes": 2,
            "recommended_frequency_per_week": 3,
            "allowed_slots": ["lunch", "evening"],
            "intensity": "light",
            "fallback_candidate_id": None,
        },
        {
            "candidate_id": "bedtime_wind_down",
            "category": "sleep",
            "trigger": "bedtime_alarm",
            "standard_minutes": 10,
            "minimum_minutes": 3,
            "recommended_frequency_per_week": 5,
            "allowed_slots": ["evening"],
            "intensity": "light",
            "fallback_candidate_id": "dim_lights",
        },
        {
            "candidate_id": "dim_lights",
            "category": "sleep",
            "trigger": "bedtime_alarm",
            "standard_minutes": 3,
            "minimum_minutes": 1,
            "recommended_frequency_per_week": 5,
            "allowed_slots": ["evening"],
            "intensity": "light",
            "fallback_candidate_id": None,
        },
    ],
    "busy_user": [
        {
            "candidate_id": "bedtime_wind_down",
            "category": "sleep",
            "trigger": "bedtime_alarm",
            "standard_minutes": 8,
            "minimum_minutes": 3,
            "recommended_frequency_per_week": 5,
            "allowed_slots": ["night"],
            "intensity": "light",
            "fallback_candidate_id": "dim_lights",
        },
        {
            "candidate_id": "dim_lights",
            "category": "sleep",
            "trigger": "bedtime_alarm",
            "standard_minutes": 3,
            "minimum_minutes": 1,
            "recommended_frequency_per_week": 5,
            "allowed_slots": ["night"],
            "intensity": "light",
            "fallback_candidate_id": None,
        },
        {
            "candidate_id": "water_after_first_meal",
            "category": "hydration",
            "trigger": "after_first_meal",
            "standard_minutes": 1,
            "minimum_minutes": 1,
            "recommended_frequency_per_week": 7,
            "allowed_slots": ["afternoon"],
            "intensity": "light",
            "fallback_candidate_id": "water_bottle_visible",
        },
        {
            "candidate_id": "water_bottle_visible",
            "category": "hydration",
            "trigger": "start_work",
            "standard_minutes": 1,
            "minimum_minutes": 1,
            "recommended_frequency_per_week": 7,
            "allowed_slots": ["afternoon"],
            "intensity": "light",
            "fallback_candidate_id": None,
        },
    ],
}


@mcp.tool()
def get_health_profile(user_id: UserId) -> dict:
    """사용자의 목표, 시간 제약, 선호, 안전 제한을 조회합니다."""
    return {
        "user_id": user_id,
        **deepcopy(_PROFILES[user_id]),
        "source": "demo-health-profile",
    }


@mcp.tool()
def get_recent_habit_summary(user_id: UserId, days: int = 7) -> dict:
    """최근 습관 기록을 성공률, 평균, 실패 이유 category로 요약합니다."""
    if not 1 <= days <= 30:
        raise ValueError("days는 1 이상 30 이하여야 합니다.")

    records = _HISTORY[user_id][-days:]
    planned = [record for record in records if record["planned"]]
    completed = [record for record in planned if record["completed"]]
    failure_reasons = Counter(
        record["failure_reason"]
        for record in planned
        if not record["completed"] and record["failure_reason"] is not None
    )
    successful_contexts = sorted({
        record["context"]
        for record in completed
        if record["context"] is not None
    })

    return {
        "user_id": user_id,
        "requested_days": days,
        "analyzed_days": len(records),
        "planned_attempts": len(planned),
        "completed_attempts": len(completed),
        "completion_rate": round(len(completed) / len(planned), 2) if planned else None,
        "average_sleep_hours": round(
            mean(record["sleep_hours"] for record in records),
            1,
        ),
        "average_energy_level": round(
            mean(record["energy_level"] for record in records),
            1,
        ),
        "failure_reason_counts": dict(sorted(failure_reasons.items())),
        "successful_contexts": successful_contexts,
        "source": "demo-habit-history",
    }


@mcp.tool()
def get_habit_candidates(user_id: UserId) -> dict:
    """사용자 제약 안에서 조합할 수 있는 안전한 습관 행동 블록을 조회합니다."""
    return {
        "user_id": user_id,
        "items": deepcopy(_CANDIDATES[user_id]),
        "source": "demo-habit-catalog",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
