import gzip
import json
from typing import Dict

import boto3

from loader.loaders.aws_ec2 import AmazonEC2Loader
from loader.loaders.base_loader import BaseLoader
from loader.s3iterator import BucketIterator
from secret import AWS_ACCESS_KEY_ID, AWS_SECRET, AWS_BUCKET_NAME


class Loader:
    def __init__(self):
        self._session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET
        )

        self.s3client = self._session.client('s3')

        self.loaders: Dict[str, BaseLoader] = {
            # TODO Fill in with all loaders
            'AmazonEC2': AmazonEC2Loader()
        }

    def already_loaded(self, filename: str) -> bool:
        """
        Check the database for whether a file has already been loaded.
        """
        # TODO implement this
        return False

    def mark_loaded(self, filename: str):
        """
        Mark in the database that a file has been loaded, so that it will not be loaded again.
        """
        # TODO implement this
        pass

    def load_file(self, filename: str):
        self.s3client.download_file(AWS_BUCKET_NAME, filename, 'tmp-loading.json.gz')

        loader_name = filename.split('/')[0]

        with gzip.open('tmp-loading.json.gz', 'rt', encoding='ascii') as f_in:
            content = json.load(f_in)
            self.loaders[loader_name].load(content)

        self.mark_loaded(filename)

    def load_initial_data(self):
        for file in BucketIterator(self.s3client, AWS_BUCKET_NAME):
            filename = file['Key']
            if self.already_loaded(filename):
                continue

            self.load_file(filename)
