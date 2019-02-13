from abc import abstractmethod
import datetime

from crawler.s3upload import upload_file_from_url


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
    def crawl(self):
        pass

    def upload_provider_data(self, region: str, url: str):
        return upload_file_from_url(url, self.provider_name() + "/" + region + "/" +
                                    datetime.datetime.utcnow().isoformat() + ".json")
