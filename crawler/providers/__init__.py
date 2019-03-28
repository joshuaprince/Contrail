from __future__ import annotations

import datetime
import importlib
import os
from abc import abstractmethod, ABC
from typing import Set, Type, List

from crawler.s3upload import upload_file_from_url, upload_file_from_variable


class BaseProvider(ABC):
    """
    Represents a cloud service provider, such as AWS or Azure. Any derived provider must be registered with the
    crawler with @register_provider for the crawler to crawl this provider.
    """

    @classmethod
    @abstractmethod
    def create_providers(cls) -> List[BaseProvider]:
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

    def upload_provider_data(self, region: str, url: str = None, data=None):
        if url is not None:
            return upload_file_from_url(url, self.provider_name() + "/" + region + "/" +
                                        datetime.datetime.utcnow().isoformat() + ".json")
        if data is not None:
            return upload_file_from_variable(data, self.provider_name() + "/" + region + "/" +
                                             datetime.datetime.utcnow().isoformat() + ".json")

        raise ValueError("Must specify either a URL or data dictionary to upload.")


REGISTERED_PROVIDER_CLASSES: Set[Type[BaseProvider]] = set()


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
