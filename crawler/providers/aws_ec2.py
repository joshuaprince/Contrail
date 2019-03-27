import datetime
import json
import logging
import urllib.request

from crawler.providers import BaseProvider, register_provider

logger = logging.getLogger('contrail.crawler.aws_ec2')

URL_REGION_INDEX = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/region_index.json'
"""
URL for the region index json, which lists all regions and the URLs to use for each
"""

URL_REGION_VERSION = 'https://pricing.us-east-1.amazonaws.com{currentVersionUrl}'
"""
URL to use for getting all data about a single region. Replaces {currentVersionUrl} with the url obtained in
region_index.
"""


@register_provider
class AmazonEC2(BaseProvider):
    def __init__(self):
        super().__init__()

        self.regions = {}

        self.load_regions()

    @classmethod
    def create_providers(cls):
        return [cls()]

    def crawl(self) -> datetime.timedelta:
        """
        Pulls data from the first region in `self.regions` and removes it from the list. If the region list is empty,
        this will load new regions instead.
        :return:
        """
        if len(self.regions) == 0:
            self.load_regions()
            return datetime.timedelta(hours=12)

        region = self.regions.pop(next(iter(self.regions)))

        self.upload_provider_data(region=region['regionCode'],
                                  url=URL_REGION_VERSION.format(currentVersionUrl=region['currentVersionUrl']))

        return datetime.timedelta(seconds=10)

    def load_regions(self):
        logger.info("Getting AWS region list")

        region_request = urllib.request.urlopen(URL_REGION_INDEX)
        region_data = region_request.read().decode('utf-8')
        region_json = json.loads(region_data)

        self.regions = region_json['regions']

        logger.info("Got {} AWS regions".format(len(self.regions)))
