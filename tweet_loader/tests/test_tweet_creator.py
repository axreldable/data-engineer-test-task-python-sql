from json import JSONDecodeError
from unittest import TestCase

from tweet_loader.sentiment import SentimentCounterFactory
from tweet_loader.tests.helper import read_file
from tweet_loader.tweet import Tweet, Location, User
from tweet_loader.tweet import TweetCreator


class TestTweetCreator(TestCase):
    tweet_creator = TweetCreator(SentimentCounterFactory.from_dict({
        'tweet': -2,
        'text': 1,
        'message': 0,
    }))

    def test_create_tweet_full(self):
        json_tweet = read_file('./files/tweet_full.json')

        expected_tweet = Tweet(text='tweet text message',
                               lang='ar',
                               sentiment=-1,
                               created_at='Sun Aug 16 21:41:13 +0000 2015',
                               location=Location(name='Texas',
                                                 county_code='US'),
                               user=User('user name'))

        result_tweet = self.tweet_creator.create(json_tweet)

        self.assertEqual(expected_tweet, result_tweet)

    def test_create_tweet_wrong_json(self):
        tweet_json = 'wrong_json'

        self.assertRaises(JSONDecodeError, self.tweet_creator.create, tweet_json)
