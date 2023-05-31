import sqlite3
import psycopg2
import os
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
from collections import defaultdict
from dataclasses import astuple, asdict
from tables import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

TABLES = {
    "film_work": Filmwork,
    "genre": Genre,
    "genre_film_work": GenreFilmwork,
    "person": Person,
    "person_film_work": PersonFilmwork
}

class SQLiteExtractor:
    def __init__(self, connection):
        self.connection = connection

    def extract_table(self, table: str, batchsize: int):
        try:
            curs = self.connection.cursor()
            query = f"SELECT * FROM {table};"
            dataclass = TABLES.get(table)
            curs.execute(query)

            batch_data = defaultdict(list)
            columns_name = None
            while True:
                rows = curs.fetchmany(batchsize)
                print(f"Got {table} with {len(rows)} rows")
                if not rows:
                    break
                for row in rows:
                    data = dataclass(*row)
                    if not columns_name:
                        columns_name = data.__annotations__.keys()
                    batch_data[table].append(astuple(data))
            return batch_data, columns_name

        except sqlite3.Error as e:
            print(e)


class PostgresSaver:

    def __init__(self, connection: _connection):
        self.connection = connection

    def save_all_data(self, data: dict, columns: tuple):
        try:
            cursor = self.connection.cursor()
            columns_placeholders = ', '.join(tuple(columns))
            for table, rows in data.items():
                num_columns = len(columns)
                value_placeholders = ', '.join(['%s'] * num_columns)
                query = f'INSERT INTO content.{table} ({columns_placeholders})' \
                        f' VALUES ({value_placeholders}) ON CONFLICT (id) DO NOTHING;'
                cursor.executemany(query, rows)
            self.connection.commit()
        except sqlite3.Error as e:
            print(e)


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    load_dotenv()
    batchsize = int(os.getenv("BATCHSIZE"))

    for table in TABLES:
        data, columns = sqlite_extractor.extract_table(table, batchsize)
        postgres_saver.save_all_data(data, columns)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)

