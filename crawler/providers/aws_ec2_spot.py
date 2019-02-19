import datetime
import logging

import boto3

from crawler.providers.base_provider import BaseProvider
from secret import AWS_ACCESS_KEY_ID, AWS_SECRET

_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET
)


class AmazonEC2Spot(BaseProvider):
    """
    Price crawler for Amazon Spot Instances.

    Each crawler object crawls only one region. Since boto3 (and Amazon's web API) imposes a 1000-row limit on the
    number of instances that can be returned in a single query, retrieving a single "batch" of instances takes multiple
    crawling cycles.
    """
    def __init__(self, region_name):
        super().__init__()

        self.region = region_name
        self.client = _session.client('ec2', region_name=region_name)

        self.logger = logging.getLogger('contrail.crawler.aws_ec2_spot.{region}'.format(region=self.region))

        self.instance_list = []
        self.next_token = ''
        """Working list of currently available instances in this region."""

    def crawl(self):
        """
        Collects the next set of instances in this region and appends them to the current `instance_list`.

        If there are no more instances in the current batch, finalize and upload the current `instance_list` instead.
        """
        if self.next_token == '' and len(self.instance_list) > 0:
            self.logger.info("Got all instances in this batch. Finalizing batch for upload.")
            self.upload_provider_data(region=self.region, data=self.instance_list)
            self.instance_list.clear()
            return

        response = self.client.describe_spot_price_history(
            NextToken=self.next_token,
            StartTime=datetime.datetime.now()  # TODO: Get all data since the last time the crawler ran
        )

        # JSON can't serialize datetime objects, so convert them before save
        for instance in response['SpotPriceHistory']:
            instance['Timestamp'] = instance['Timestamp'].isoformat()

        self.next_token = response['NextToken']
        self.instance_list += response['SpotPriceHistory']

        self.logger.info("Retrieved {count} instances".format(region=self.region,
                                                              count=len(response['SpotPriceHistory'])))

    @classmethod
    def create_providers(cls):
        return [AmazonEC2Spot(rgn) for rgn in _session.get_available_regions('ec2')]
