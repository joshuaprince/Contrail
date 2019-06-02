import gzip
import json
import logging
import shutil
import urllib.request

import boto3

from contrail.configuration import config

logger = logging.getLogger('contrail.crawler')


class S3Client:
    _session = boto3.Session(
        aws_access_key_id=config['AWS']['access_key_id'],
        aws_secret_access_key=config['AWS']['secret']
    )

    _client = _session.client('s3')

    def upload_file_from_url(self, url: str, destination: str):
        """
        Pulls data from a certain URL, compresses it, and uploads it to S3.

        :param url: URL to pull data from.
        :param destination: Path within S3 to store data
        :return:
        """
        logger.info("Uploading file {} to {}".format(url, destination))

        tmpfile = "tmp.json"
        zipfile = tmpfile + ".gz"

        urllib.request.urlretrieve(url, tmpfile)

        # source: https://docs.python.org/3/library/gzip.html
        with open(tmpfile, 'rb') as f_in:
            with gzip.open(zipfile, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        self._client.upload_file(zipfile, config['AWS']['bucket_name'], destination + ".gz")

    def upload_file_from_variable(self, data: dict, destination: str):
        """
        Takes data formatted as a Python dictionary, serializes it to JSON,
        compresses this JSON file, and uploads it to S3.

        :param data: The dictionary/list/object to serialize to JSON.
        :param destination: Path within S3 to store data.
        """
        logger.info("Uploading raw data to {}".format(destination))

        tmpfile = "tmp-rawdata.json"
        zipfile = tmpfile + ".gz"

        # source: https://stackoverflow.com/questions/49534901/is-there-a-way-to-use-json-dump-with-gzip
        with gzip.open(zipfile, 'wt', encoding='ascii') as f_out:
            json.dump(data, f_out, indent=2)

        self._client.upload_file(zipfile, config['AWS']['bucket_name'], destination + ".gz")
