from unittest import TestCase

from tweet_loader.loader import TweetLoader
from tweet_loader.tweet import Tweet, User


class TestTweetLoader(TestCase):
    loader = TweetLoader(tweets_file_path='./files/tweets_in_line.txt',
                         sentiment_file_path='./files/sentiment_file_correct.txt',
                         sql_lite_db_file_path='./db/tweets.db')

    def test_read_tweets(self):
        expected_tweets = [
            Tweet(text='tweet text message',
                  lang='ar',
                  sentiment=-1,
                  created_at='Sun Aug 16 21:41:13 +0000 2015',
                  location=None,
                  user=User('user name'))
        ]

        tweets = self.loader._read_tweets(tweets_file_path='./files/tweets_in_line.txt',
                                          sentiment_counter=self.loader.sentiment_counter)

        self.assertListEqual(expected_tweets, tweets)
