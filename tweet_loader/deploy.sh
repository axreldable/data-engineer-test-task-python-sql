#!/usr/bin/env bash

# for local testing

set -eu

TEST_DIR=/Users/user/delete_me/test_mts/
SPATH=$(dirname $0)

rsync -vaz ${SPATH}/dist/tweet-loader-1.0.0.tar.gz ${TEST_DIR}

rsync -vaz ${SPATH}/../task/three_minutes_tweets.json ${TEST_DIR}
rsync -vaz ${SPATH}/../task/AFINN-111.txt ${TEST_DIR}
rsync -vaz ${SPATH}/tests/empty_db/empty_tweets.db ${TEST_DIR}/tweets.db

rsync -vaz ${SPATH}/logging.ini ${TEST_DIR}
