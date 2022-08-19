import psycopg2
from psycopg2 import Error
import asyncio
import asyncpg
import json


from main import aio_http_session
from config import user, password, host, port, database

# Подключиться к существующей базе данных
# connection = psycopg2.connect(user=user,
#                               # пароль, который указали при установке PostgreSQL
#                               password=password,
#                               host=host,
#                               port=port,
#                               database=database)
#
# cursor = connection.cursor()


def postgres_connect():
    try:
        # Подключиться к существующей базе данных
        connection = psycopg2.connect(user=user,
                                      # пароль, который указали при установке PostgreSQL
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        # Создайте курсор для выполнения операций с базой данных
        cursor = connection.cursor()
        # SQL-запрос для создания новой таблицы
        create_table_query = """CREATE TABLE IF NOT EXISTS SWAPI_db(
                                id INT PRIMARY KEY,
                                name TEXT,
                                birth_year TEXT,
                                eye_color TEXT,
                                films TEXT,
                                gender TEXT,
                                hair_color TEXT,
                                height TEXT,
                                homeworld TEXT,
                                mass TEXT,
                                skin_color TEXT,
                                species TEXT,
                                starships TEXT,
                                vehicles TEXT);
                            """
        # Выполнение команды: это создает новую таблицу
        cursor.execute(create_table_query)
        connection.commit()
        print("Таблица успешно создана в PostgreSQL")


    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)



async def create_table():
    connection = await asyncpg.connect(user=user,
                                          # пароль, который указали при установке PostgreSQL
                                          password=password,
                                          host=host,
                                          port=port,
                                          database=database)

    async with connection.transaction():
        cur = connection.cursor("SELECT * FROM SWAPI_db")

        if cur is None:
            for k, v in aio_http_session.items():
                for i in v:
                    await connection.execute(f"""INSERT INTO SWAPI_db (id, name, birth_year, eye_color, films, gender, hair_color,
                                    height, homeworld, mass, skin_color, species, starships, vehicles)
                                    VALUES('{k}', '{i['name']}', '{i['birth_year']}', '{i['eye_color']}', '{json.dumps(i['films'])}',
                                    '{i['gender']}','{i['hair_color']}', '{i['height']}', '{json.dumps(i['homeworld'])}', '{i['mass']}',
                                    '{json.dumps(i['skin_color'])}', '{json.dumps(i['species'])}', '{json.dumps(i['starships'])}',
                                    '{json.dumps(i['vehicles'])}');""")

                    # connection.commit()
            print("Данные добавлены!")
                    # await connection.close()

        # connection.fetch("SELECT * FROM SWAPI_db")
        # record = connection.fetchall()
        #     res = await connection.fetch("SELECT * FROM SWAPI_db")

        #     return res

async def get_date_swapi():
        date = []
        connection = await asyncpg.connect(user=user,
                                              # пароль, который указали при установке PostgreSQL
                                              password=password,
                                              host=host,
                                              port=port,
                                              database=database)

        cur = await connection.fetch("SELECT * FROM SWAPI_db")
        for i in cur:
            date.append(i[0:14])
        return date



postgresql_connect = postgres_connect()  # Создание таблицы
create_table = asyncio.get_event_loop().run_until_complete(create_table())  # Добавление значений в таблицу
get_date_swapi = asyncio.get_event_loop().run_until_complete(get_date_swapi())  # Вывод данных из таблицы

print(get_date_swapi)