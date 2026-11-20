from src.api_connector import GetCoordinate, InfoPlanes
from src.config import COUNTRIES
from src.utils import create_database, create_tables, insert_data
from src.connect_bd import DBConnector
from src.config import db_config
from src.db_manager import DBManager


if __name__ == '__main__':
    # Подключение к API сервисам и получение данных
    api = GetCoordinate(COUNTRIES)
    coord = api.get_api_request()
    opensky_api = InfoPlanes(coord)

    # Создание базы данных и подключение к ней
    db_name = 'course_3_test'
    create_database(db_name)
    test_config = {**db_config, 'dbname': db_name}
    connector = DBConnector(test_config)
    # Создание нужных таблиц и заполнение их
    create_tables(connector)
    insert_data(connector)

    # Вывод всех стран и количество самолетов в их воздушных пространствах
    manager = DBManager(connector)
    countries_with_count = manager.get_countries_and_aeroplanes_count()
    print(f'{"Страна":<15} | {"Количество самолетов":>20}')
    print('-' * 45)

    for country, count in countries_with_count:
        print(f"{country:<15} | {count:>20}")

    print('_' * 45)

    # Вывод всех воздушных судов, без повторений позывных
    all_aircraft = manager.get_all_aeroplanes()
    for plane in all_aircraft:
        id_plane = plane[0] if plane[0] is not None else '-'
        country_id = plane[1] if plane[1] is not None else '-'
        callsign = plane[2] if plane[2] is not None else '-'
        on_ground = str(plane[3]) if plane[3] is not None else '-'
        velocity = plane[4] if plane[4] is not None else '-'
        altitude = plane[5] if plane[5] is not None else '-'


        print(f'{id_plane:^6} | {country_id:^5} | {callsign:^12} | {on_ground:^6} | {velocity:>8} | {altitude:>8}')

    print('_' * 45)

    # Вывод средней скорости самолетов по странам
    avg_speed = manager.get_avg_speed()
    for speed in avg_speed:
        country_id = speed[0] if speed[0] is not None else '-'
        avg_str = round(speed[1],2) if speed[1] is not None else '-'

        print(f'{country_id:^6} | {avg_str:^8}')

    print('_' * 45)

    # Вывод всех самолетов, у которых скорость выше средней
    list_aircraft = manager.get_aeroplanes_with_higher_speed()
    for list in list_aircraft:
        id_plane = list[0] if list[0] is not None else '-'
        country_id = list[1] if list[1] is not None else '-'
        callsign = list[2] if list[2] is not None else '-'
        on_ground = str(list[3]) if list[3] is not None else '-'
        velocity = list[4] if list[4] is not None else '-'
        altitude = list[5] if list[5] is not None else '-'

        print(f'{id_plane:^6} | {country_id:^5} | {callsign:^12} | {on_ground:^6} | {velocity:>8} | {altitude:>8}')

    print('_' * 45)

    # Вывод всех самолетов, в позывном которых содержатся переданные в метод символы
    plane = manager.get_aeroplanes_with_keyword('aca')
    for pl in plane[:10]:
        id_pl = pl[0] if pl[0] is not None else '-'
        country_id = pl[1] if pl[1] is not None else '-'
        callsign = pl[2] if pl[2] is not None else '-'
        on_ground = str(pl[3]) if pl[3] is not None else '-'
        velocity = pl[4] if pl[4] is not None else '-'
        altitude = pl[5] if pl[5] is not None else '-'

        print(f'{id_pl:^6} | {country_id:^5} | {callsign:^12} | {on_ground:^6} | {velocity:>8} | {altitude:>8}')
