from tweet_loader.exceptions import TweetLoaderException
from tweet_loader.file import read_lines_from_file


class _SentimentCounter:
    def __init__(self, sentiment_dict: dict):
        self.sentiment_dict = sentiment_dict

    def count(self, text: str) -> int:
        """
        Counts sentiment in the text according to the sentiment_dict.

        :param text: a text for sentiment counting
        :return: amount of sentiment in the text
        """
        words = text.split(' ')

        result_sentiment = 0
        for word in words:
            sentiment = self.sentiment_dict.get(word)

            if sentiment is not None:
                result_sentiment += sentiment

        return result_sentiment


class SentimentCounterFactory:
    DEFAULT_SEPARATOR = '\t'

    @staticmethod
    def _create_dict_from_file(file_path: str, separator: chr) -> dict:
        """
        Create a sentiment dict from file.

        :param file_path: a path to the file with key value pairs in each line
        :param separator: a separator between the key and the value
        :return: result dict
        """
        result_dict = {}

        try:
            lines = read_lines_from_file(file_path)
            for line in lines:
                word, sentiment = line.split(separator)
                result_dict[word] = int(sentiment)
        except ValueError:
            raise TweetLoaderException(f'Failed to create a dict from the file {file_path}!')

        return result_dict

    @staticmethod
    def from_file(file_path: str, separator=DEFAULT_SEPARATOR):
        sentiment_dict = SentimentCounterFactory._create_dict_from_file(file_path, separator)

        return _SentimentCounter(sentiment_dict)

    @staticmethod
    def from_dict(sentiment_dict: dict):
        return _SentimentCounter(sentiment_dict)
