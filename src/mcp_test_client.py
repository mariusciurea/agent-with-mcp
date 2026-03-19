import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


BASE_DIR = Path(__file__).resolve().parent
SERVER_PATH = BASE_DIR / "mcp_car_server.py"


READ_TEST = {
    "brand": "Toyota",
    # Optional:
    # "model": "RAV4",
    # "manufacture_year": 2022,
}

RUN_WRITE_TEST = True
WRITE_TEST = {
    "brand": "TestBrand",
    "price": 12345.0,
    "seats": 5,
    "manufacture_year": 2026,
}


def _safe_dump(value: Any) -> str:
    if hasattr(value, "model_dump"):
        return json.dumps(value.model_dump(), indent=2, ensure_ascii=False, default=str)
    if hasattr(value, "dict"):
        return json.dumps(value.dict(), indent=2, ensure_ascii=False, default=str)
    if isinstance(value, (dict, list)):
        return json.dumps(value, indent=2, ensure_ascii=False, default=str)
    return str(value)


def _format_tool_response(call_result: Any) -> str:
    content = getattr(call_result, "content", None)
    if not content:
        return _safe_dump(call_result)

    chunks: list[str] = []
    for item in content:
        text = getattr(item, "text", None)
        if text is not None:
            chunks.append(text)
        else:
            chunks.append(_safe_dump(item))
    return "\n".join(chunks)


async def run_client() -> None:
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to MCP server.\n")

            tools_result = await session.list_tools()
            print("Exposed tools:")
            for tool in tools_result.tools:
                description = tool.description or "No description."
                print(f"- {tool.name}: {description}")

            print("\nReading cars with get_car_details...")
            read_result = await session.call_tool(
                "get_car_details", arguments=READ_TEST
            )
            print(_format_tool_response(read_result))

            if RUN_WRITE_TEST:
                print("\nWriting a test car with add_car_details...")
                suffix = datetime.now().strftime("%Y%m%d%H%M%S")
                model_name = f"TestModel_{suffix}"
                add_args = {
                    "brand": WRITE_TEST["brand"],
                    "model": model_name,
                    "price": WRITE_TEST["price"],
                    "seats": WRITE_TEST["seats"],
                    "manufacture_year": WRITE_TEST["manufacture_year"],
                }
                add_result = await session.call_tool(
                    "add_car_details", arguments=add_args
                )
                print(_format_tool_response(add_result))

                print("\nVerifying inserted car with get_car_details...")
                verify_result = await session.call_tool(
                    "get_car_details",
                    arguments={
                        "brand": WRITE_TEST["brand"],
                        "model": model_name,
                        "manufacture_year": WRITE_TEST["manufacture_year"],
                    },
                )
                print(_format_tool_response(verify_result))


def main() -> None:
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
