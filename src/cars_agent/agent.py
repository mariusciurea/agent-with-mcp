import os
import sys
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters


BASE_DIR = Path(__file__).resolve().parent.parent
MCP_SERVER_PATH = BASE_DIR / "mcp_car_server.py"

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="car_assistant",
    instruction=(
        "You are a car assistant. "
        "When the user asks for car details, use the tool "
        "'get_car_details'. "
        "When the user asks to add a car to the database, use the tool "
        "'add_car_details'. "
        "Always answer in English and clearly present the tool result."
    ),
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command=sys.executable,
                    args=[str(MCP_SERVER_PATH)],
                    env=os.environ.copy(),
                ),
            ),
        )
    ],
)
