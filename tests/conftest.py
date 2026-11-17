import pytest
import json

from typing import Any

@pytest.fixture
def coordinates() -> dict:
    return {"lamin": "41.6765597", "lamax": "83.3362128", "lomin": "-141.00275", "lomax": "-52.3237664"}


@pytest.fixture
def nominatim() -> list[dict]:
    return [{"boundingbox": ["41.6765597", "83.3362128", "-141.00275", "-52.3237664"]}]


@pytest.fixture
def without_coordinate() -> list[dict]:
    return [{"boundingbox": []}]


@pytest.fixture
def error_nominatim() -> list[dict]:
    return [{"boundingbox": ["41.6765597", "83.3362128", "-141.00275"]}]


@pytest.fixture
def aircraft() -> dict[str, Any]:
    return json.loads("""{
        "time": 1766166618,
        "states": [
            ["4b1812", "SWR438A", "United States", 1766166618, 1766166618,
            -0.0168, 51.0888, 4267.2, false, 189.7, 129.39, 14.63,
            null, 4282.44, "2061", false, 0]
            ]
    }
    """)