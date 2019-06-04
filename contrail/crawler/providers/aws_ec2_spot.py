import datetime
import json
import logging
import urllib.request
from typing import List

import boto3

from contrail.configuration import config
from contrail.crawler.providers import aws_ec2
from contrail.crawler.providers import BaseProvider, register_provider

logger_all_regions = logging.getLogger('contrail.crawler.aws_ec2_spot')

_session = boto3.Session(
    aws_access_key_id=config['AWS']['access_key_id'],
    aws_secret_access_key=config['AWS']['secret']
)

# AWS Price List retrieval information, used to collect details about instance types.
URL_REGION_INDEX = aws_ec2.URL_REGION_INDEX
URL_REGION_VERSION = aws_ec2.URL_REGION_VERSION
DETAIL_COLLECTION_REGION = 'us-east-1'


@register_provider
class AmazonEC2Spot(BaseProvider):
    """
    Price crawler for Amazon Spot Instances.

    Each crawler object crawls only one region. Since boto3 (and Amazon's web API) imposes a 1000-row limit on the
    number of instances that can be returned in a single query, retrieving a single "batch" of instances takes multiple
    crawling cycles.
    """
    instance_types = {}

    def __init__(self, region_name):
        super().__init__()

        self.region = region_name
        self.client = _session.client('ec2', region_name=region_name)

        self.logger = logging.getLogger('contrail.crawler.aws_ec2_spot.{region}'.format(region=self.region))

        self.instance_list = []
        """Working list of currently available instances in this region."""
        self.next_token = ''
        """Token given to AWS to continue building instance_list."""

    @classmethod
    def create_providers(cls) -> List['AmazonEC2Spot']:
        return [AmazonEC2Spot(rgn) for rgn in _session.get_available_regions('ec2')]

    def crawl(self) -> datetime.timedelta:
        """
        Collects the next set of instances in this region and appends them to the current `instance_list`.

        If there are no more instances in the current batch, finalize and upload the current `instance_list` instead.
        """

        if not self.__class__.instance_types:
            self.__class__.instance_types = self.__class__.get_instance_type_details()

        if self.next_token == '' and len(self.instance_list) > 0:
            self.logger.info("Got all instances in this batch. Finalizing batch for upload.")
            self.store_provider_data(region=self.region, data=self.instance_list)
            self.instance_list.clear()
            return datetime.timedelta(minutes=60)

        response = self.client.describe_spot_price_history(
            NextToken=self.next_token,
            StartTime=datetime.datetime.now() - datetime.timedelta(minutes=60)
        )

        for instance in response['SpotPriceHistory']:
            # JSON can't serialize datetime objects, so convert them before save
            instance['Timestamp'] = instance['Timestamp'].isoformat()

            # Attach instance type information
            instance_type = instance.get('InstanceType')
            if instance_type is None:
                continue
            type_data = self.__class__.instance_types.get(instance_type)
            if type_data is None:
                continue
            instance.update(type_data)

        self.next_token = response['NextToken']
        self.instance_list += response['SpotPriceHistory']

        self.logger.info("Retrieved {count} instances".format(region=self.region,
                                                              count=len(response['SpotPriceHistory'])))
        return datetime.timedelta(seconds=3)

    @classmethod
    def get_instance_type_details(cls) -> dict:
        """
        Load a dictionary that maps instance type names (e.g. 'm2.large') to instance details such as vCPUs, RAM, etc.
        """
        region_request = urllib.request.urlopen(URL_REGION_INDEX)
        region_data = region_request.read().decode('utf-8')
        region_json = json.loads(region_data)

        current_price_list_url = URL_REGION_VERSION.format(
            currentVersionUrl=region_json['regions'][DETAIL_COLLECTION_REGION]['currentVersionUrl']
        )

        pricelist_request = urllib.request.urlopen(current_price_list_url)
        pricelist_data = pricelist_request.read().decode('utf-8')
        pricelist_json = json.loads(pricelist_data)

        instance_types = {}

        for _sku, data in pricelist_json['products'].items():
            instance_type = data['attributes'].get('instanceType')

            if instance_type is None:
                continue

            if instance_types.get(instance_type) is None:
                # Remove data that does not apply to all instances of this type
                for k in ['location', 'locationType']:
                    data['attributes'].pop(k)

                instance_types[instance_type] = data['attributes']
            else:
                for attribute, value in data['attributes'].items():
                    existing_attr = instance_types[instance_type].get(attribute)

                    # Only collect instance type details that are universal across all instances with that type.
                    # Therefore, if a detail on one instance mismatches an earlier instance's detail, remove it --
                    # the detail is not common to that instance type.
                    if existing_attr is not None and existing_attr != value:
                        instance_types[instance_type].pop(attribute)

        logger_all_regions.info("Loaded instance type information.")

        return instance_types
