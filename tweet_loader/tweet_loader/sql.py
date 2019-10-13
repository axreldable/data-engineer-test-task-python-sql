import logging
import sqlite3
from abc import abstractmethod

from tweet_loader.exceptions import TweetLoaderException

logger = logging.getLogger(__name__)


class InsertObject:
    """
    Represents an object which will be insert into a database.
    """

    @abstractmethod
    def table_name(self) -> str:
        """
        :return: a name of the table or view to insert
        """
        pass

    @abstractmethod
    def to_tuple(self) -> tuple:
        """
        :return: a tuple representation of the object
        """
        pass


class SqLiteInserter:
    def __init__(self, db_file):
        self.conn = self._create_connection(db_file)

    def close_connection(self):
        self.conn.close()

    def _create_connection(self, db_file):
        try:
            conn = sqlite3.connect(db_file)
        except sqlite3.Error:
            logger.error(f'Failed to connect to sqlite {db_file}')
            raise TweetLoaderException(f'Failed to connect to sqlite {db_file}')

        return conn

    def insert_many(self, objects: list):
        if len(objects) == 0:
            logger.warning('Try to insert empty list of objects!')
            return None

        logger.debug(f'Trying to insert {len(objects)} objects...')

        table_name = objects[0].table_name()

        insert_tuples_iter = map(lambda obj: obj.to_tuple(), objects)

        cur = self.conn.cursor()
        # cur.executemany(f'INSERT INTO {table_name} VALUES', insert_tuples)
        for it in insert_tuples_iter:
            logger.debug(f'INSERT INTO {table_name} VALUES {it}')
            cur.execute(f'INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?)', it)

        self.conn.commit()
        logger.debug(f'Insert {len(objects)} objects successfully.')
        return cur.lastrowid

    def insert_one(self, obj: InsertObject) -> str:
        return self.insert_many([obj])
