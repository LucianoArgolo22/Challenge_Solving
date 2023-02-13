from psycopg2 import OperationalError, errorcodes, errors
import psycopg2
import json
import pandas as pd
import sys

path = '/'.join(__file__.split('/')[:-2])

with open(f'{path}/utils/psql_config.json', 'r') as file:
    data = file.read()
    data = json.loads(data)


class ClientPSQL:
    def __init__(self, log:object, table:str = None, df:pd.DataFrame = None, conn_config:dict = None):
        self.log = log
        self.conn = self.connector()
        self.df = df
        self.table = table
        self.conn_config = conn_config

    def show_psycopg2_exception(self, err):
        err_type, traceback = sys.exc_info()
        line_n = traceback.tb_lineno

        self.log.info("psycopg2 ERROR:", err, "on line number:", line_n)
        self.log.info("psycopg2 traceback:", traceback, "-- type:", err_type)
        self.log.info("extensions.Diagnostics:", err.diag)
        self.log.info("pgerror:", err.pgerror)
        self.log.info("pgcode:", err.pgcode)

    def connector(self) -> object:
            conn = None
            try:
                self.log.info('Connecting to the PostgreSQL...........')
                conn = psycopg2.connect(**data)
                self.log.info("Connection successful..................")
            except OperationalError as err:
                self.show_psycopg2_exception(err)
                conn = None
            return conn
    
    def generating_fields(self) -> str:
        self.log.info(f'Generating fields:{list(self.df.keys())}')
        return ','.join(list(self.df.keys()))

    def generating_values(self) -> str:
        self.log.info('Generating Values')
        return ','.join(['%s' for _ in range(len(self.df.keys()))])

    def insert_query(self) -> str:
        query = f"""INSERT into {self.table} ({self.generating_fields()})
                                        VALUES ({self.generating_values()})"""
        self.log.info(f'Generating Query: {query}')
        return query


    def inserting_rows(self) -> None:
        records_to_insert = [tuple(x) for x in self.df.to_numpy()]
        sql = self.insert_query()
        cursor = self.conn.cursor()
        self.log.info(f'Inserting records')
        try:
            while records_to_insert:
                if 30000 < len(records_to_insert):
                    cursor.executemany(sql, records_to_insert[0:30000])
                    records_to_insert = records_to_insert[30000:]
                else:
                    cursor.executemany(sql, records_to_insert)
                    records_to_insert = []
            self.conn.commit()
            self.log.info("Data inserted using execute_many() successfully...")
        except (Exception, psycopg2.DatabaseError) as err:
            self.show_psycopg2_exception(err)   
            cursor.close()


