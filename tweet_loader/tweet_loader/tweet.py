import json
import logging.config
from datetime import datetime
from pprint import pformat

from tweet_loader.exceptions import TweetLoaderException
from tweet_loader.sentiment import _SentimentCounter
from tweet_loader.sql import InsertObject

logger = logging.getLogger(__name__)


class Country:
    def __init__(self, name: str, code: str):
        self.name = name
        self.code = code

    def __eq__(self, other):
        if isinstance(other, Country):
            return self.name == other.name and \
                   self.code == other.code
        return False

    def __repr__(self):
        return pformat(vars(self))


class Location:
    def __init__(self, name: str, county: Country):
        self.name = name
        self.county = county

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.name == other.name and \
                   self.county == other.county
        return False

    def __repr__(self):
        return pformat(vars(self))


class User:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, User):
            return self.name == other.name
        return False

    def __repr__(self):
        return pformat(vars(self))


class Tweet(InsertObject):
    source_datetime_format = '%a %b %d %H:%M:%S %z %Y'
    result_datetime_format = '%Y-%m-%d %H:%M:%S %z'

    def table_name(self) -> str:
        return 'tweets_for_insert'

    def to_tuple(self) -> tuple:
        location_name = None
        country_name = None
        country_code = None

        if self.location is not None:
            location_name = self.location.name
            country_name = self.location.county.name
            country_code = self.location.county.code

        return (
            self.text,
            self.lang,
            self.sentiment,
            self.created_at,
            location_name,
            country_name,
            country_code,
            self.user.name,
        )

    def _converter_datetime(self, date_time_str: str, source_format: str, dest_format: str) -> str:
        """
        Converts string datetime from one format to another.

        :param date_time_str: a beginning datetime
        :param source_format: a beginning format
        :param dest_format: a result format
        :return: a datetime with result format
        """
        try:
            dt = datetime.strptime(date_time_str, source_format)
        except ValueError:
            raise TweetLoaderException(f'Input datetime format should be \'{self.source_datetime_format}\'.')
        return dt.strftime(dest_format)

    def __init__(self, text: str, lang: str, sentiment: int, created_at: str, user: User, location):
        """
        :param text: a text of the tweet
        :param lang: a language of the tweet
        :param sentiment: a sentiment appraisal of the tweet
        :param created_at: datetime of the creation of the tweet
        :param user: a user who wrote the tweet (users with different names are different users)
        :param location: a location of the tweet (can be empty)
        """
        self.text = text
        self.sentiment = sentiment
        self.lang = lang
        self.created_at = self._converter_datetime(date_time_str=created_at,
                                                   source_format=self.source_datetime_format,
                                                   dest_format=self.result_datetime_format)
        self.location = location
        self.user = user

    def __eq__(self, other):
        if isinstance(other, Tweet):
            return self.text == other.text and \
                   self.lang == other.lang and \
                   self.sentiment == other.sentiment and \
                   self.created_at == other.created_at and \
                   self.location == other.location and \
                   self.user == other.user
        return False

    def __repr__(self):
        return pformat(vars(self))


class TweetCreator:
    def __init__(self, sentiment_counter: _SentimentCounter):
        self.sentiment_counter = sentiment_counter

    def create(self, json_tweet: str):
        """
        Creates a Tweet from a json tweet representation.

        :param json_tweet: a json tweet representation
        :return: constructed Tweet
        """
        tweet_dict = json.loads(json_tweet)
        logger.debug(f'Trying to create tweet from dict: {tweet_dict}')

        if tweet_dict.get('delete') is not None:
            return None

        text = tweet_dict['text']
        lang = tweet_dict['lang']
        sentiment = self.sentiment_counter.count(text)
        created_at = tweet_dict['created_at']

        location = None
        location_dict = tweet_dict.get('place')
        if location_dict is not None:
            country = Country(name=location_dict['country'],
                              code=location_dict['country_code'])

            location = Location(name=location_dict['name'],
                                county=country)

        user = User(name=tweet_dict['user']['name'])

        result_tweet = Tweet(text=text,
                             lang=lang,
                             sentiment=sentiment,
                             created_at=created_at,
                             location=location,
                             user=user)
        logger.debug(f'Tweet creating result: {result_tweet}')

        return result_tweet
