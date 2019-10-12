import os
import shutil
import sqlite3
from unittest import TestCase

from tweet_loader.sql import SqLiteInserter
from tweet_loader.tweet import Tweet, Location, User, Country


class TestTweetWorker(TestCase):
    tweet_db_path = './db/tweets.db'
    inserter = None

    def setUp(self):
        """
        Creates an empty sqlite db for testing
        """
        shutil.copyfile('./empty_db/empty_tweets.db', self.tweet_db_path)

        self.inserter = SqLiteInserter(self.tweet_db_path)

    def tearDown(self):
        """
        Deletes testing sqlite db
        """
        self.inserter.close_connection()

        if os.path.exists(self.tweet_db_path):
            os.remove(self.tweet_db_path)

    def test_insert_one(self):
        tweet = Tweet(text='tweet text message',
                      lang='ar',
                      sentiment=22,
                      created_at='Sun Aug 16 21:41:13 +0300 2015',
                      location=Location(name='Texas',
                                        county=Country(name='United States',
                                                       code='US')),
                      user=User('user name'))

        row_id = self.inserter.insert_one(tweet)

        expected_row_id = 0
        self.assertEqual(expected_row_id, row_id)

        conn = sqlite3.connect(self.tweet_db_path)
        with conn:
            cur = conn.cursor()

            tweet_tuples = cur.execute('SELECT * FROM tweets').fetchall()
            self.assertEqual(1, len(tweet_tuples))

            expected_tweet_tuple = (1, 'tweet text message', 22, 'ar', '2015-08-16 21:41:13 +0300', 1, 1)
            self.assertEqual(expected_tweet_tuple, tweet_tuples[0])

    def test_insert_many(self):
        self.inserter = SqLiteInserter(self.tweet_db_path)

        tweets = [
            Tweet(text='tweet text message 1',
                  lang='ar',
                  sentiment=22,
                  created_at='Sun Aug 16 21:41:13 +0300 2015',
                  location=Location(name='Texas',
                                    county=Country(name='United States',
                                                   code='US')),
                  user=User('Alex')),
            Tweet(text='tweet text message 2',
                  lang='en',
                  sentiment=1,
                  created_at='Sun Aug 16 22:41:13 +0000 2015',
                  location=Location(name='Falkirk',
                                    county=Country(name='???',
                                                   code='GB')),
                  user=User('John')),
            Tweet(text='tweet text message 3',
                  lang='ar',
                  sentiment=13,
                  created_at='Sun Aug 16 23:41:13 +0000 2015',
                  location=Location(name='Texas',
                                    county=Country(name='United States',
                                                   code='US')),
                  user=User('Alex')),
        ]

        row_id = self.inserter.insert_many(tweets)

        expected_row_id = 0
        self.assertEqual(expected_row_id, row_id)

        conn = sqlite3.connect(self.tweet_db_path)
        with conn:
            cur = conn.cursor()

            tweet_tuples = cur.execute('SELECT * FROM tweets').fetchall()
            self.assertEqual(3, len(tweet_tuples))
            expected_tweet_tuples = [
                (1, 'tweet text message 1', 22, 'ar', '2015-08-16 21:41:13 +0300', 1, 1),
                (2, 'tweet text message 2', 1, 'en', '2015-08-16 22:41:13 +0000', 2, 2),
                (3, 'tweet text message 3', 13, 'ar', '2015-08-16 23:41:13 +0000', 1, 1),
            ]
            self.assertListEqual(expected_tweet_tuples, tweet_tuples)

            user_tuples = cur.execute('SELECT * FROM users').fetchall()
            self.assertEqual(2, len(user_tuples))
            expected_user_tuples = [
                (1, 'Alex'),
                (2, 'John'),
            ]
            self.assertListEqual(expected_user_tuples, user_tuples)

            location_tuples = cur.execute('SELECT * FROM locations').fetchall()
            self.assertEqual(2, len(location_tuples))
            expected_location_tuples = [
                (1, 'Texas', 1),
                (2, 'Falkirk', 2),
            ]
            self.assertListEqual(expected_location_tuples, location_tuples)
