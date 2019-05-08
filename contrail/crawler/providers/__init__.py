import datetime
import importlib
import os
from abc import abstractmethod, ABC
from typing import Set, Type, Iterable

from contrail.crawler.s3upload import S3Client

s3client = S3Client()


class BaseProvider(ABC):
    """
    Represents a cloud service provider, such as AWS or Azure. Any derived provider must be registered with the
    crawler with @register_provider for the crawler to crawl this provider.
    """

    @classmethod
    @abstractmethod
    def create_providers(cls) -> Iterable['BaseProvider']:
        """
        Create a list of Provider objects for this class, each of which are crawled separately.
        If multiple servers or regions are being crawled, each should have a single Provider object.
        :return:
        """
        return []

    @classmethod
    def provider_name(cls) -> str:
        """
        A name for this provider, defaults to the class name.
        """
        return cls.__name__

    @abstractmethod
    def crawl(self) -> datetime.timedelta:
        """
        This function will be called every x amount of time. It should return a timedelta that indicates how long it
        would like the program to wait before calling it again.
        """
        pass

    def store_provider_url(self, region: str, url: str):
        """
        Store raw data directly from a web URL.
        """
        return s3client.upload_file_from_url(url, self.provider_name() + "/" + region + "/" +
                                             datetime.datetime.utcnow().isoformat() + ".json")

    def store_provider_data(self, region: str, data):
        """
        Store data formatted as a Python object.
        """
        return s3client.upload_file_from_variable(data, self.provider_name() + "/" + region + "/" +
                                                  datetime.datetime.utcnow().isoformat() + ".json")


REGISTERED_PROVIDER_CLASSES = set()  # type: Set[Type[BaseProvider]]
"""
A set consisting of all classes that have been registered with `@register_provider`.
"""


def register_provider(cls: Type[BaseProvider]):
    """
    Decorator to register a subclass of BaseProvider. Example usage:
        @register_provider
        class MyProvider(BaseProvider):
            ...
    """
    REGISTERED_PROVIDER_CLASSES.add(cls)
    return cls


def import_provider_directory():
    """
    Imports all files in the [Contrail]/crawler/providers directory to ensure that they are registered.
    :return:
    """
    for fl in os.listdir(os.path.dirname(__file__)):
        if os.path.basename(fl).endswith('.py') and not os.path.basename(fl).startswith('__'):
            importlib.import_module('.' + os.path.basename(fl)[:-3], package=__package__)
