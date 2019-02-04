import gzip
import logging
import shutil
import urllib.request

import boto3

from secret import AWS_ACCESS_KEY_ID, AWS_SECRET, AWS_BUCKET_NAME

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
    logging.info("Uploading file {} to {}".format(url, destination))

    tmpfile = "tmp.json"
    zipfile = tmpfile + ".gz"

    urllib.request.urlretrieve(url, tmpfile)

    # source: https://docs.python.org/3/library/gzip.html
    with open(tmpfile, 'rb') as f_in:
        with gzip.open(zipfile, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    _client.upload_file(zipfile, AWS_BUCKET_NAME, destination + ".gz")
