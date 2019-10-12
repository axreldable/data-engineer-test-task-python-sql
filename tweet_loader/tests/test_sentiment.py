from unittest import TestCase

from tweet_loader.exceptions import TweetLoaderException
from tweet_loader.sentiment import SentimentCounterFactory


class TestSentimentCounter(TestCase):
    def test_create_dict_from_file(self):
        sentiment_dict = SentimentCounterFactory._create_dict_from_file('./files/sentiment_file_correct.txt', '\t')

        expected_dict = {
            'tweet': -2,
            'text': 1,
            'message': 0,
        }

        self.assertEqual(expected_dict, sentiment_dict)

    def test_create_dict_from_file_wrong_words_in_line(self):
        self.assertRaises(TweetLoaderException, SentimentCounterFactory._create_dict_from_file,
                          './files/sentiment_file_wrong_words_in_line.txt', '\t')

    def test_create_dict_from_file_not_number_sentiment(self):
        self.assertRaises(TweetLoaderException, SentimentCounterFactory._create_dict_from_file,
                          './files/sentiment_file_not_number_sentiment.txt', '\t')

    def test_count_empty(self):
        empty_text = ''

        sentiment_counter = SentimentCounterFactory.from_file('./files/sentiment_file_correct.txt')
        sentiment = sentiment_counter.count(empty_text)

        expected_sentiment = 0

        self.assertEqual(expected_sentiment, sentiment)

    def test_count(self):
        empty_text = 'tweet text message another_word'

        sentiment_dict = {
            'tweet': -2,
            'text': 1,
            'message': 0,
        }

        sentiment_counter = SentimentCounterFactory.from_dict(sentiment_dict)
        sentiment = sentiment_counter.count(empty_text)

        expected_sentiment = -1

        self.assertEqual(expected_sentiment, sentiment)

    def test_count_sentiment_empty_dict(self):
        sentiment_counter = SentimentCounterFactory.from_dict({})

        self.assertEqual(0, sentiment_counter.count('random text'))

    def test_count_sentiment_no_same_words(self):
        sentiment_counter = SentimentCounterFactory.from_dict({
            'word1': 1,
            'word2': 1,
        })

        self.assertEqual(0, sentiment_counter.count('random text'))

    def test_count_sentiment_empty_text(self):
        sentiment_counter = SentimentCounterFactory.from_dict({
            'word1': 1,
            'word2': 1,
        })

        self.assertEqual(0, sentiment_counter.count(''))

    def test_count_sentiment(self):
        sentiment_counter = SentimentCounterFactory.from_dict({
            'some': 1,
            'message': 1,
        })

        self.assertEqual(2, sentiment_counter.count('some message'))
