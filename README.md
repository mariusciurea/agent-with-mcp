# Python app with Google ADK + MCP (cars)

This app includes:
- one Google ADK agent (`cars_agent/agent.py`)
- one MCP server (`mcp_car_server.py`) with 2 tools
- one JSON file (`data/cars.json`) with 30 cars

## Exposed MCP tools

1. `get_car_details`
- reads car data by `brand` and optional `model` / `manufacture_year`

2. `add_car_details`
- adds a new car to `data/cars.json` with:
  - `brand`
  - `model`
  - `price`
  - `seats`
  - `manufacture_year`

## Installation

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Gemini API key setup

1. Copy `.env.example` to `.env`
2. Fill in `GOOGLE_API_KEY`

## Run the agent

Run from the project folder:

```bash
adk run cars_agent
```

Or with the web interface:

```bash
adk web --no-reload
```

In `adk web`, select the `cars_agent` agent.

## Example prompts

Reading:
- `Show me details for the Toyota RAV4.`
- `What BMW cars from year 2023 do you have?`

Writing:
- `Add a new car: brand Renault, model Clio, price 17900, 5 seats, manufacture year 2024.`

The agent will automatically use the correct MCP tools based on prompt intent.

## MCP test client module

You can test the MCP server directly with:

```bash
python mcp_test_client.py
```

This client will:
- connect to `mcp_car_server.py`
- initialize an MCP session
- list exposed tools
- call `get_car_details`

By default, the client also runs a write test (calls `add_car_details` and verifies insert).

To change test behavior, edit the settings at the top of `mcp_test_client.py`:
- `READ_TEST` for read arguments
- `RUN_WRITE_TEST` to enable/disable write test
- `WRITE_TEST` for write arguments
