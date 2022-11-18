import pandas as pd
from sqlalchemy import create_engine


class Loader:
    def __init__(self, user, password, host, database, port, batch_size):
        self.user = user
        self.password = password
        self.host = host
        self.database = database
        self.port = port
        self.batch_size = batch_size
        self.offset = 0
        self.database_uri = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}?charset=utf8mb4"
        self.engine = create_engine(self.database_uri, pool_recycle=1800)

    def load_batch(self, offset, count):
        response = self.engine.execute(
            f'select post_text, comment_text FROM posts limit {offset}, {count}').fetchall()
        X = [row[0] for row in response]
        y = [row[1] for row in response]
        return (X, y)

    def __iter__(self):
        self.offset = 0
        return self

    def __next__(self):
        res = self.load_batch(self.offset, self.batch_size)
        self.offset += self.batch_size
        if len(res) == 0:
            raise StopIteration
        return res
