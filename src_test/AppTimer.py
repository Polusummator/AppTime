from time import sleep
from typing import *
import os
import sqlite3
from GetAppName import get_active_app


class DB:
    def __init__(self, path: str, txt: str, table: str) -> None:
        self.table = table
        self.connect_create_table(path, txt)

    def connect_create_table(self, path: str, txt: str):
        with open(path, 'a'):
            pass
        self.conn = sqlite3.connect(path)
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute(txt)
            self.conn.commit()
        except sqlite3.OperationalError:
            pass

    def insert(self, **kwargs) -> NoReturn:
        # args : {id, app, usage}
        self.cursor.execute("INSERT INTO '{table}' VALUES ({id}, '{app}', {usage});".format(table=self.table, **kwargs))
        self.conn.commit()

    def update(self, **kwargs) -> NoReturn:
        # args : {upd, new_value, con, app}
        self.cursor.execute("UPDATE '{table}' SET {upd} = {new_value} WHERE {con} = '{app}';".format(table=self.table, **kwargs))
        self.conn.commit()

    def select(self, **kwargs) -> list:
        # args : {sel, con, app}
        if kwargs['sel'] == '*':
            self.cursor.execute("SELECT * FROM '{table}';".format(table=self.table), kwargs)
        else:
            self.cursor.execute("SELECT {sel} FROM '{table}' WHERE {con} = '{app}';".format(table=self.table, **kwargs))
        result = self.cursor.fetchall()
        return result

    def close_db(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    table = 'apptable'
    create_text = """
                  CREATE TABLE {} (
                  id INTEGER,
                  app TEXT,
                  usage INTEGER,
                  PRIMARY KEY (id)
                  );
                  """.format(table)

    db = DB('./data/UsageTime.db', create_text, table)
    while True:
        app = get_active_app()
        where = db.select(sel='usage', con='app', app=app)
        print('where', where)
        if not where:
            last = db.select(sel='*')
            print('last', last)
            if not last:
                last_id = 1
            else:
                last_id = last[-1][0]+1
            print('last_id', last_id)
            db.insert(id=last_id, app=app, usage=1)
            print('insert')
        else:
            db.update(upd='usage', new_value=where[0][0]+1, con='app', app=app)
        # print(app)
        # print(where)
        print('ALL', db.select(sel='*'))
        try:
            sleep(1)
        except KeyboardInterrupt:
            pass
            exit(0)
