from abc import abstractmethod
import datetime

from crawler.s3upload import upload_file_from_url, upload_file_from_variable


class BaseProvider:
    """
    Represents a cloud service provider, such as AWS or Azure. Any derived provider must be registered with the
    crawler with crawler.register_provider() for the crawler to crawl this provider.
    """

    @classmethod
    def provider_name(cls):
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
