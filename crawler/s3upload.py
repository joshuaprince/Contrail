import gzip
<<<<<<< HEAD
import json
=======
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
import logging
import shutil
import urllib.request

import boto3

from secret import AWS_ACCESS_KEY_ID, AWS_SECRET, AWS_BUCKET_NAME

<<<<<<< HEAD
logger = logging.getLogger('contrail.crawler')

=======
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET
)

_client = _session.client('s3')


def upload_file_from_url(url: str, destination: str):
    """
    Pulls data from a certain URL, compresses it, and uploads it to S3.
    :param url: URL to pull data from.
    :param destination: Path within S3 to store data
    :return:
    """
<<<<<<< HEAD
    logger.info("Uploading file {} to {}".format(url, destination))
=======
    logging.info("Uploading file {} to {}".format(url, destination))
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9

    tmpfile = "tmp.json"
    zipfile = tmpfile + ".gz"

    urllib.request.urlretrieve(url, tmpfile)

    # source: https://docs.python.org/3/library/gzip.html
    with open(tmpfile, 'rb') as f_in:
        with gzip.open(zipfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    _client.upload_file(zipfile, AWS_BUCKET_NAME, destination + ".gz")
<<<<<<< HEAD


def upload_file_from_variable(data: dict, destination: str):
    """
    Takes data formatted as a Python dictionary, serializes it to JSON,
    compresses this JSON file, and uploads it to S3.
    :param data: The dictionary to serialize to JSON.
    :param destination: Path within S3 to store data.
    """
    logger.info("Uploading raw data to {}".format(destination))

    tmpfile = "tmp-rawdata.json"
    zipfile = tmpfile + ".gz"

    # source: https://stackoverflow.com/questions/49534901/is-there-a-way-to-use-json-dump-with-gzip
    with gzip.open(zipfile, 'wt', encoding='ascii') as f_out:
        json.dump(data, f_out)

    _client.upload_file(zipfile, AWS_BUCKET_NAME, destination + ".gz")
=======
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
