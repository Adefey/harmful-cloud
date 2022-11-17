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

    def load_batch(self, count):
        df = pd.read_sql(f'select post_text, comment_text FROM posts limit {self.offset}, {count}', con = self.engine)
        self.offset += count
        return df

    def __iter__(self):
        self.offset = 0
        return self

    def __next__(self):
        df = self.load_batch(self.batch_size)
        if len(df) == 0:
            raise StopIteration
        return df
