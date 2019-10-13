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

    def _questions_str(self, question_amount) -> str:
        """
        Creates question string parameter.

        Ex:
            - question_amount = 5
            - result = (?, ?, ?, ?, ?)

            - question_amount = 0
            - result = ()

        :param question_amount: an amount of question in str
        :return:
        """
        if question_amount <= 0:
            return '()'

        questions = ', '.join('?' * question_amount)
        return f'({questions})'

    def insert_many(self, objects: list):
        if len(objects) == 0:
            logger.warning('Try to insert empty list of objects!')
            return None

        logger.debug(f'Trying to insert {len(objects)} objects...')

        table_name = objects[0].table_name()
        params_amount = len(objects[0].to_tuple())

        insert_tuples = list(map(lambda obj: obj.to_tuple(), objects))

        cur = self.conn.cursor()
        cur.executemany(f'INSERT INTO {table_name} VALUES {self._questions_str(params_amount)}', insert_tuples)

        self.conn.commit()
        logger.debug(f'Insert {len(objects)} objects successfully.')

    def insert_one(self, obj: InsertObject):
        return self.insert_many([obj])
