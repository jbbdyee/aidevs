"""부산과 서울의 관광지 정보를 제공하는 교육용 stdio MCP Server입니다."""

from typing import Literal

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    "tour",
    instructions="부산과 서울의 대표 관광지 정보를 제공합니다.",
)

ATTRACTIONS = {
    "부산": [
        {
            "name": "해운대 해수욕장",
            "category": "해변",
            "description": "넓은 백사장과 해안 산책로로 유명한 부산의 대표 해수욕장입니다.",
        },
        {
            "name": "감천문화마을",
            "category": "문화마을",
            "description": "산복도로를 따라 이어지는 다채로운 골목과 전망을 즐길 수 있습니다.",
        },
        {
            "name": "태종대",
            "category": "자연",
            "description": "해안 절벽과 숲길에서 탁 트인 바다 풍경을 감상할 수 있습니다.",
        },
    ],
    "서울": [
        {
            "name": "경복궁",
            "category": "궁궐",
            "description": "조선 시대의 역사와 전통 건축을 살펴볼 수 있는 대표 궁궐입니다.",
        },
        {
            "name": "북촌 한옥마을",
            "category": "전통문화",
            "description": "한옥과 골목이 어우러진 서울의 전통 주거 문화를 만날 수 있습니다.",
        },
        {
            "name": "남산서울타워",
            "category": "전망대",
            "description": "서울 도심을 한눈에 조망할 수 있는 남산의 대표 명소입니다.",
        },
    ],
}


@mcp.tool()
def get_tourist_attractions(location: Literal["부산", "서울"]) -> dict:
    """지명으로 대표 관광지 정보를 조회합니다."""
    return {
        "location": location,
        "items": ATTRACTIONS[location],
        "source": "lab-tour-catalog",
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
