import psycopg2

from src.api_connector import GetCoordinate, InfoPlanes
from src.config import COUNTRIES, db_config
from src.connect_bd import DBConnector


def create_database(dbname):
    conn = psycopg2.connect(dbname="postgres", **db_config)
    cursor = conn.cursor()
    conn.autocommit = True

    cursor.execute(f"DROP DATABASE IF EXISTS {dbname}")
    cursor.execute(f"CREATE DATABASE {dbname}")

    cursor.close()
    conn.close()


def create_tables(connector):
    connector.execute(
        """CREATE TABLE IF NOT EXISTS countries (
            id SERIAL PRIMARY KEY,
            name VARCHAR (255) NOT NULL UNIQUE
            )""",
        (),
    )

    connector.execute(
        """CREATE TABLE IF NOT EXISTS aircraft (
            id SERIAL PRIMARY KEY,
            country_id INT,
            callsign VARCHAR (50) NOT NULL,
            on_ground BOOL NOT NULL,
            velocity NUMERIC,
            altitude NUMERIC,
            CONSTRAINT fk_countries_aircraft FOREIGN KEY (country_id) REFERENCES countries (id)
            )""",
        (),
    )


def insert_data(connector):
    for country in COUNTRIES:
        result = connector.fetch_one(
            """
                INSERT INTO countries (name) VALUES (%s) RETURNING id""",
            (country,),
        )
        if result is not None:
            country_id = result[0]
        else:
            print(f"Страна {country} не добавилась или уже существует")

    aircraft = InfoPlanes(GetCoordinate(COUNTRIES).get_api_request()).get_api_request()

    for country, aircraft_list in aircraft.items():
        result_country = connector.fetch_one(
            """
                SELECT id FROM countries WHERE name = %s""",
            (country,),
        )
        if result_country is not None:
            target_country_id = result_country[0]

            for plane in aircraft_list:
                connector.execute(
                    """
                        INSERT INTO aircraft (country_id, callsign, on_ground, velocity, altitude)
                        VALUES (%s, %s, %s, %s, %s)""",
                    (
                        target_country_id,
                        plane["callsign"],
                        str(plane["on_ground"]).lower(),
                        plane["velocity"],
                        plane["altitude"],
                    ),
                )
        else:
            print(f"Страна {country} не добавилась или уже существует")


if __name__ == "__main__":
    db_name = "course_3_test"
    create_database(db_name)
    test_config = {**db_config, "dbname": db_name}
    connector = DBConnector(test_config)
    create_tables(connector)
    insert_data(connector)

    table_result = connector.fetch_all("SELECT * FROM aircraft LIMIT 1")
    countries = connector.fetch_all("SELECT * FROM countries")
    print(table_result)
    print(countries)
