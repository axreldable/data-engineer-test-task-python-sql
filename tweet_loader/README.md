# tweet_loader

A python project to loads tweets from file to sqlite db.

### How to install
1. package the loader in archive
```
python setup.py sdist
```
2. create environment, for example conda environment
3. install the loader and all needed dependencies
```
conda create -n env-test python=3.7
pip install tweet-loader-<version>.tar.gz
```

### How to use
1. Run the tweet_loader command which is available in the environment
```
conda activate env-test
tweet_loader --tweet_file_path ./three_minutes_tweets.json --sentiment_file_path ./AFINN-111.txt --sql_lite_db_file_path ./tweets.db
```
