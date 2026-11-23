class DBManager:
    """Принимает коннектор к базе данных и возвращает:
    -  список всех стран и количество самолетов в их воздушных пространствах
    - список всех воздушных судов
    - среднюю скорость по самолетам
    - список всех самолетов, у которых скорость выше средней
    - список всех самолетов, в позывном которых содержатся переданные в метод символы"""

    def __init__(self, connector):
        self._connector = connector

    def get_countries_and_aeroplanes_count(self) -> list:
        query = """SELECT name, COUNT(aircraft.country_id) AS count_aircraft FROM countries
                   LEFT JOIN aircraft ON aircraft.country_id = countries.id
                   GROUP BY countries.name
                   ORDER BY count_aircraft DESC"""

        result = self._connector.fetch_all(query)
        return list(result)

    def get_all_aeroplanes(self) -> list:
        query = """SELECT DISTINCT ON (callsign) * FROM aircraft
                   ORDER BY callsign, id DESC"""
        all_aircraft = self._connector.fetch_all(query)
        return list(all_aircraft)

    def get_avg_speed(self) -> list:
        query = """SELECT countries.name, AVG(aircraft.velocity) AS avg_velocity FROM aircraft
                JOIN countries ON countries.id = aircraft.country_id
                WHERE aircraft.velocity IS NOT NULL
                GROUP BY countries.id
                ORDER BY avg_velocity DESC"""

        avg_speed = self._connector.fetch_all(query)
        return list(avg_speed)

    def get_aeroplanes_with_higher_speed(self) -> list:
        query = """SELECT * FROM aircraft
                   WHERE velocity > (SELECT AVG(velocity) FROM aircraft)
                   ORDER BY velocity"""

        list_aicraft = self._connector.fetch_all(query)
        return list(list_aicraft)

    def get_aeroplanes_with_keyword(self, keyword: str) -> list:
        word = f"%{keyword.lower()}%"
        query = """SELECT * FROM aircraft
                   WHERE LOWER(callsign) LIKE LOWER(%s)
                   ORDER BY callsign"""

        aircraft_with_word = self._connector.fetch_all(query, (word,))
        return list(aircraft_with_word)
