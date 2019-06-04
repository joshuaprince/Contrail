import datetime
import gzip
import json
import logging
import sys

import boto3

from contrail.configuration import config
from contrail.loader.loaders import REGISTERED_LOADER_CLASSES, import_loader_directory, LoaderDoesNotExistError
from contrail.loader.s3iterator import BucketIterator
from contrail.loader.warehouse import create_contrail_table, db, LoadedFile

logger = logging.getLogger('contrail.loader')


class Loader:
    def __init__(self):
        self._session = boto3.Session(
            aws_access_key_id=config['AWS']['access_key_id'],
            aws_secret_access_key=config['AWS']['secret']
        )

        self.s3client = self._session.client('s3')

    def already_loaded(self, filename: str) -> bool:
        """
        Check the database for whether a file has already been loaded.
        """
        return LoadedFile.objects_in(db).filter(filename=filename).count() > 0

    def mark_loaded(self, filename: str):
        """
        Mark in the database that a file has been loaded, so that it will not be loaded again.
        """
        db.insert([LoadedFile(filename=filename, time_loaded=datetime.datetime.now())])

    def load_file(self, filename: str, last_modified: str):
        loader_name = filename.split('/')[0]

        if not REGISTERED_LOADER_CLASSES.get(loader_name):
            raise LoaderDoesNotExistError(loader_name)

        logger.info("Downloading file {}".format(filename))
        self.s3client.download_file(config['AWS']['bucket_name'], filename, 'tmp-loading.json.gz')

        with gzip.open('tmp-loading.json.gz', 'rt', encoding='ascii') as f_in:
            content = json.load(f_in)
            REGISTERED_LOADER_CLASSES[loader_name].load(filename, content, last_modified, db)

        self.mark_loaded(filename)

    def load_initial_data(self):
        for file in BucketIterator(self.s3client, config['AWS']['bucket_name']):
            filename = file['Key']
            last_modified = file['LastModified']

            if self.already_loaded(filename):
                continue

            try:
                self.load_file(filename, last_modified)
            except Exception as e:
                logger.warning("Failed to load data file {}:\n{}".format(filename, str(e)))
                logger.exception(e)


def load():
    root_logger = logging.getLogger('contrail')
    root_logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(logging.Formatter(fmt=logging.BASIC_FORMAT))
    root_logger.addHandler(stream_handler)

    import_loader_directory()
    logger.info("Loaded {} loaders.".format(len(REGISTERED_LOADER_CLASSES)))
    logger.debug(list(REGISTERED_LOADER_CLASSES.keys()))

    create_contrail_table()
    Loader().load_initial_data()
