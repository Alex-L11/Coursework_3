from abc import ABC, abstractmethod
from typing import Any

import requests


class APIService(ABC):

    @abstractmethod
    def get_api_request(self) -> dict[str, Any]:
        pass


class GetCoordinate(APIService):
    """Класс для получения координат из API сервиса Nominatim"""

    def __init__(self, countries: list) -> None:
        self.__openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.countries = countries

    def _get_country_coordinate(self, country: str) -> dict[str, Any]:

        # Обязательный параметр User-Agent при запросе к nominatim.openstreetmap
        headers_nominatim = {"User-Agent": "test-app"}
        # Указываем параметры: в каком формате возвращать данные и максимальную длину списка стран в ответе.
        params_nominatim: dict[str, Any] = {
            "country": country,
            "format": "json",
            "limit": 1,
        }

        response = requests.get(
            url=self.__openstreetmap_url,
            params=params_nominatim,
            headers=headers_nominatim,
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()

        # Получение координат
        if not data:
            raise ValueError("Координаты не найдены для указанной страны")

        geo_coordinates = data[0].get("boundingbox")

        if geo_coordinates is None or len(geo_coordinates) != 4:
            raise ValueError("Некорректный формат координат")

        return {
            "lamin": geo_coordinates[0],
            "lamax": geo_coordinates[1],
            "lomin": geo_coordinates[2],
            "lomax": geo_coordinates[3],
        }

    def get_api_request(self) -> dict[str, dict[str, Any]]:
        result = {}
        for country in self.countries:
            try:
                result[country] = self._get_country_coordinate(country)
            except ValueError as ve:
                print(f"Пропускаю {country}, ошибка: \n{ve}")
        return result


class InfoPlanes(APIService):
    """Класс для получения информации о самолетах в заданных координатах"""

    def __init__(self, geo_coordinates: dict[str, Any]) -> None:
        self.__opensky_url = "https://opensky-network.org/api/states/all"
        self.geo_coordinates = geo_coordinates

    def _get_coordinate_country(
        self, geo_coordinate: dict[str, Any]
    ) -> list[dict[str, Any]]:
        params = {
            "lamin": geo_coordinate["lamin"],
            "lamax": geo_coordinate["lamax"],
            "lomin": geo_coordinate["lomin"],
            "lomax": geo_coordinate["lomax"],
        }

        response = requests.get(url=self.__opensky_url, params=params, timeout=10)
        response.raise_for_status()

        info_planes: dict = response.json()

        if "states" not in info_planes:
            raise ValueError("Неожиданный формат ответа от OpenSky")

        aircraft = []
        for plane in info_planes["states"]:
            aircraft.append(
                {
                    "ica": plane[0],
                    "callsign": plane[1].strip(),
                    "on_ground": plane[8],
                    "velocity": plane[9],
                    "altitude": plane[13],
                }
            )
        return aircraft

    def get_api_request(self) -> dict[str, Any]:
        result = {}
        for coord in self.geo_coordinates:
            try:
                result[coord] = self._get_coordinate_country(
                    self.geo_coordinates[coord]
                )
            except ValueError as ve:
                print(f"Некорректные данные в {coord}: \n{ve}")
            except requests.RequestException as re:
                print(f"ОШибка соединения: {re}")
        return result
