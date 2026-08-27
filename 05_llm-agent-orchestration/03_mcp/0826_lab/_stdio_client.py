"""건강 습관 MCP 예제가 사용하는 stdio Client 연결 도우미입니다."""

import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = Path(__file__).with_name("mcp_server.py")


@asynccontextmanager
async def connect_to_health_coach_server():
    server_env = {"PYTHONUTF8": "1"}
    if python_path := os.getenv("PYTHONPATH"):
        server_env["PYTHONPATH"] = python_path

    parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env=server_env,
    )
    async with stdio_client(parameters) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session
