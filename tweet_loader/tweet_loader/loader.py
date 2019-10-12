import logging

from tweet_loader.file import read_lines_from_file
from tweet_loader.sentiment import SentimentCounterFactory, _SentimentCounter
from tweet_loader.sql import SqLiteInserter
from tweet_loader.tweet import TweetCreator

logger = logging.getLogger(__name__)


class TweetLoader:
    def __init__(self, tweets_file_path: str, sentiment_file_path: str, sql_lite_db_file_path: str):
        self.tweets_file_path = tweets_file_path
        self.sentiment_counter = SentimentCounterFactory.from_file(sentiment_file_path)
        self.sql_inserter = SqLiteInserter(sql_lite_db_file_path)

    def _read_tweets(self, tweets_file_path: str, sentiment_counter: _SentimentCounter) -> list:
        """
        Reads Tweets from the tweets_file_path.

        :param tweets_file_path: a path to the file with tweets as json
        :param sentiment_counter: an object which can count sentiment
        :return: a list of Tweets
        """
        json_tweets = read_lines_from_file(tweets_file_path)

        tweet_creator = TweetCreator(sentiment_counter)

        tweets = []
        for json_tweet in json_tweets:
            tweet = tweet_creator.create(json_tweet)

            if tweet is not None:
                tweets.append(tweet)

        return tweets

    def load(self):
        logger.info(f'Starting loading tweets from {self.tweets_file_path}...')
        tweets = self._read_tweets(self.tweets_file_path, self.sentiment_counter)
        logger.info('Successfully read tweets.')

        logger.info(f'Starting loading tweets to sqlite...')
        self.sql_inserter.insert_many(tweets)
        logger.info('Successfully insert tweets.')
