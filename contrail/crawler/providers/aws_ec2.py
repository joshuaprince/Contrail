import datetime
import json
import logging
import urllib.request
from typing import List

from contrail.crawler.providers import BaseProvider, register_provider

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
    """
    This provider collects pricing data for Amazon Web Services' EC2.

    All worldwide EC2 pricing is stored in one place in the US East 1 AWS region. Each crawl cycle starts by calling
    a "region index" endpoint that lists all regions and their respective pricing URLs.
    """

    def __init__(self):
        super().__init__()

        self.region_queue = {}

        # Load regions immediately so that first crawl doesn't wait 12 hours
        self.load_regions()

    @classmethod
    def create_providers(cls) -> List['AmazonEC2']:
        return [cls()]

    def crawl(self) -> datetime.timedelta:
        """
        Pulls data from the first region in `self.regions` and removes it from the region queue.
        If the region list is empty, this will load new regions instead.

        :return: 12 hours if we reloaded region data, or 10 seconds if there are still regions to be crawled in this
        queue.
        """
        if not self.region_queued():
            self.load_regions()

        next_region = self.get_next_region()

        self.store_provider_url(region=next_region['regionCode'],
                                url=URL_REGION_VERSION.format(currentVersionUrl=next_region['currentVersionUrl']))

        if self.region_queued():
            return datetime.timedelta(seconds=10)
        else:
            return datetime.timedelta(hours=12)

    def load_regions(self):
        """
        Queries AWS API to get a list of AWS region name/pricing URL pairs, and stores them in a region queue.
        """
        logger.info("Loading AWS region list...")

        region_request = urllib.request.urlopen(URL_REGION_INDEX)
        region_data = region_request.read().decode('utf-8')
        region_json = json.loads(region_data)

        self.region_queue = region_json['regions']

        logger.info("Got {} AWS regions.".format(len(self.region_queue)))

    def get_next_region(self):
        """
        Pop the next region and its price data URL from the region queue.
        :return: The next crawlable region as a dictionary, or None if the region queue is empty.
        """
        if not self.region_queued():
            return None

        return self.region_queue.pop(next(iter(self.region_queue)))

    def region_queued(self) -> bool:
        """
        Returns true if there is still a region in the queue waiting to be crawled.
        """
        return len(self.region_queue) > 0
