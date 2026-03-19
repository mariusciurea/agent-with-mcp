"""Settings"""
from pathlib import Path
from pydantic_settings import BaseSettings

from dotenv import load_dotenv


class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MCP_SERVER_PATH: Path = BASE_DIR / "src/mcp_car_server.py"
    CARS_FILE = BASE_DIR / "data" / "cars.json"


settings = Settings()

load_dotenv(settings.BASE_DIR / ".env")
