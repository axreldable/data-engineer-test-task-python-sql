from unittest import TestCase

from tweet_loader.exceptions import TweetLoaderException
from tweet_loader.tweet import Tweet, Location, User, Country


class TestTweet(TestCase):
    tweet = Tweet(text='tweet text message',
                  lang='ar',
                  sentiment=-1,
                  created_at='Sun Aug 16 21:41:13 +0000 2015',
                  location=Location(name='Texas',
                                    county=Country(name='United States',
                                                   code='US')),
                  user=User('user name'))

    empty_location_tweet = Tweet(text='tweet text message',
                                 lang='ar',
                                 sentiment=-1,
                                 created_at='Sun Aug 16 21:41:13 +0000 2015',
                                 location=None,
                                 user=User('user name'))

    def test_converter_datetime(self):
        source_datetime = 'Sun Aug 16 21:41:13 +0300 2015'
        source_format = '%a %b %d %H:%M:%S %z %Y'
        dest_format = '%Y-%m-%d %H:%M:%S %z'

        result_datetime = self.tweet._converter_datetime(date_time_str=source_datetime,
                                                         source_format=source_format,
                                                         dest_format=dest_format)

        expected_date_time = '2015-08-16 21:41:13 +0300'

        self.assertEqual(expected_date_time, result_datetime)

    def test_converter_datetime_error(self):
        source_datetime = 'Sun Aug 16 21:41:13 +0300'
        source_format_without_year = '%a %b %d %H:%M:%S %z %Y'
        dest_format = '%Y-%m-%d %H:%M:%S %z'

        self.assertRaises(TweetLoaderException, self.tweet._converter_datetime, source_datetime,
                          source_format_without_year, dest_format)

    def test_tuple_tweet(self):
        expected_tuple = ('tweet text message', 'ar', -1, '2015-08-16 21:41:13 +0000', 'Texas', 'United States', 'US',
                          'user name')

        self.assertEqual(expected_tuple, self.tweet.to_tuple())

    def test_tuple_tweet_empty_location(self):
        expected_tuple = ('tweet text message', 'ar', -1, '2015-08-16 21:41:13 +0000', None, None, None, 'user name')

        self.assertEqual(expected_tuple, self.empty_location_tweet.to_tuple())
