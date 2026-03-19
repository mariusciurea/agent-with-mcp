import json
from typing import Any

from mcp.server.fastmcp import FastMCP

from src.settings import settings

mcp = FastMCP("car-data-server")


def _read_cars() -> list[dict[str, Any]]:
    """Read cars from json file"""
    if not settings.settings.CARS_FILE.exists():
        settings.settings.CARS_FILE.parent.mkdir(parents=True, exist_ok=True)
        settings.CARS_FILE.write_text("[]", encoding="utf-8")
        return []
    with settings.CARS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError("cars.json must contain a list.")
    return data


def _write_cars(cars: list[dict[str, Any]]) -> None:
    """Write data to json"""
    settings.CARS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with settings.CARS_FILE.open("w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=2)


@mcp.tool()
def get_car_details(
    brand: str,
    model: str | None = None,
    manufacture_year: int | None = None,
) -> dict[str, Any]:
    """
    Read car details from the JSON file.

    Args:
      brand: Car brand (required).
      model: Car model (optional).
      manufacture_year: Manufacture year (optional).
    """
    cars = _read_cars()
    results = [
        car
        for car in cars
        if car.get("brand", "").lower() == brand.lower()
        and (model is None or car.get("model", "").lower() == model.lower())
        and (
            manufacture_year is None
            or car.get("manufacture_year") == manufacture_year
        )
    ]
    return {"total_results": len(results), "cars": results}


@mcp.tool()
def add_car_details(
    brand: str,
    model: str,
    price: float,
    seats: int,
    manufacture_year: int,
) -> dict[str, Any]:
    """
    Write user-provided car details to the JSON file.

    Args:
      brand: Car brand.
      model: Car model.
      price: Car price.
      seats: Number of seats.
      manufacture_year: Manufacture year.
    """
    new_car = {
        "brand": brand,
        "model": model,
        "price": price,
        "seats": seats,
        "manufacture_year": manufacture_year,
    }
    cars = _read_cars()
    cars.append(new_car)
    _write_cars(cars)

    return {
        "status": "success",
        "message": "The car was added to cars.json.",
        "added_car": new_car,
        "total_cars": len(cars),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")
