import psycopg2
import pandas as pd
from sqlalchemy import create_engine


class DBClient():
    ''' Convenience wrapper for postgresql db instance '''

    def __init__(self, database='postgres', host='localhost', port='5432', user='postgres', password='1234') -> None:
        self.database = database
        self.host = host
        self.port = port
        self.engine = self._get_engine(user, password)

    def _get_engine(self, user, password):
        engine = create_engine(
            f'postgresql+psycopg2://{user}:{password}@{self.host}:{self.port}/{self.database}')
        return engine

    def _open_close_connection(func):
        def wraper(self, *args, **kwargs):
            conn = self.engine.connect()
            try:
                df = func(self, *args, conn=conn, **kwargs)
            finally:
                conn.close()
            return df
        return wraper

    @_open_close_connection
    def query_to_df(self, query, conn):
        print(query)
        print(conn)
        df = pd.read_sql_query(query, conn)
        return df

    @_open_close_connection
    def query(self, query, conn):
        ''' Executres any sql query. '''
        result_proxy = conn.execute(query)
        result = [dict(row) for row in result_proxy]
        return result

    @_open_close_connection
    def delete(self, table_name, conn):
        ''' Deletes a table. '''
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")

    @_open_close_connection
    def write(self, df, table_name, conn, chunksize=5000, if_exists="replace", method='multi', index=False):
        ''' writes a new table, or overwrites an existing one. '''
        df.to_sql(name=table_name, con=conn, chunksize=chunksize,
                  method=method, index=index, if_exists=if_exists)

    @_open_close_connection
    def list_tables(self, conn):
        ''' Prints a list of tables available in the database with some additional useful infomration. '''
        query = "SELECT * FROM pg_catalog.pg_tables WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';"
        df = pd.read_sql_query(query, conn)
        return df

    @_open_close_connection
    def is_not_empty(self, table_name, conn):
        query = f"SELECT COUNT(*) FROM {table_name}"
        len = pd.read_sql_query(query, conn)
        return len > 0
