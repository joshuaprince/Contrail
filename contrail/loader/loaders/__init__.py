import importlib
import os
from abc import abstractmethod, ABC
from typing import Dict, Type, Union

from infi.clickhouse_orm.database import Database

from contrail.crawler.providers import BaseProvider


class BaseLoader(ABC):
    """
    A Loader for one format of JSON file.
    """

    @classmethod
    @abstractmethod
    def load(cls, filename: str, json: dict, last_modified: str, db: Database):
        """
        Loads a single JSON file into the database. The JSON file is passed in as a dictionary.
        :param filename: Full path on S3 of the file to load.
        :param json: The contents of the file parsed as a dictionary.
        :param last_modified: Date string the file was last modified.
        :param db: ClickHouse Database object to load data into.
        """
        pass


REGISTERED_LOADER_CLASSES = {}  # type: Dict[str, Type[BaseLoader]]


def register_loader(provider: Union[Type[BaseProvider], str]):
    """
    Decorator to register a subclass of BaseLoader. Example usage:
        @register_loader(provider='aws_ec2')
        class MyLoader(BaseLoader):
            ...

    :param provider: Provider that this loader can pull data from, or a string matching the folder name in S3 where
                     data can be found for this loader.
    """
    def wrap(cls: Type[BaseLoader]):
        provider_name = provider.provider_name() if issubclass(provider, BaseProvider) else provider
        REGISTERED_LOADER_CLASSES[provider_name] = cls
        return cls
    return wrap


def import_loader_directory():
    """
    Imports all files in the [Contrail]/loader/loaders directory to ensure that they are registered.
    :return:
    """
    for fl in os.listdir(os.path.dirname(__file__)):
        if os.path.basename(fl).endswith('.py') and not os.path.basename(fl).startswith('__'):
            importlib.import_module('.' + os.path.basename(fl)[:-3], package=__package__)


class LoaderDoesNotExistError(Exception):
    """
    Raised when a file is found in an S3 directory for which no loader could be found.
    """

    def __init__(self, loader_name):
        self.loader_name = loader_name

    def __str__(self):
        return "Loader '{}' does not exist".format(self.loader_name)
