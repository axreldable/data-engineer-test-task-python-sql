# tweet_loader

A python project to loads tweets from file to sqlite db.

### how to install
1. create environment, for example conda environment
2. install the loader and all needed dependencies
```
conda create -n mts-test python=3.7
pip install tweet-loader-<version>.tar.gz
```

### how to use
1. Run the tweet_loader command which is available in the environment
```
tweet_loader --tweet_file_path ./three_minutes_tweets.json --sentiment_file_path ./AFINN-111.txt --sql_lite_db_file_path ./tweets.db --logging_conf_path ./logging.ini
```