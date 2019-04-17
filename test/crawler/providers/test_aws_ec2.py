import json
import unittest

import requests

from crawler.providers.aws_ec2 import AmazonEC2, URL_REGION_VERSION


class AmazonEC2TestCase(unittest.TestCase):
    def setUp(self):
        self.instance = AmazonEC2.create_providers()[0]

    def test_load_regions(self):
        """
        Check that the EC2 loader has correctly loaded AWS regions.
        """
        self.instance.load_regions()

        # Check for a well-known region to be in the region queue
        self.assertIn('us-west-1', self.instance.region_queue, "Couldn't find us-west-1 region.")

        # Check that get_next_region() returns at least one region before the region queue is empty.
        loaded_region = self.instance.get_next_region()
        self.assertIsNotNone(loaded_region, "No regions were loaded into AmazonEC2.regions.")

        # Loop over all regions in queue and check that currentVersionUrl is a JSON URL.
        while loaded_region is not None:
            self.assertRegex(
                loaded_region['currentVersionUrl'], r'^/.*\.json$',
                "Region {} had an invalid currentVersionUrl.".format(loaded_region)
            )
            loaded_region = self.instance.get_next_region()

    def test_file_structure(self):
        """
        Check several structural components of the raw data to ensure it is in the proper format to be loaded.
        """
        self.instance.load_regions()
        region_url_postfix = self.instance.get_next_region()['currentVersionUrl']

        response_json = requests.get(URL_REGION_VERSION.format(currentVersionUrl=region_url_postfix)).content
        response_dict = json.loads(response_json)

        self.assertEqual(response_dict['formatVersion'], 'v1.0')
        self.assertEqual(response_dict['offerCode'], 'AmazonEC2')
        self.assertIn('version', response_dict)

        self.assertIn('products', response_dict)
        for name, product in response_dict['products'].items():
            self.assertIn('sku', product)
            self.assertIn('attributes', product)
            self.assertIn('location', product['attributes'])

        self.assertIn('terms', response_dict)

        for paymentType in ('OnDemand', 'Reserved'):
            self.assertIn(paymentType, response_dict['terms'])
            for name, product in response_dict['terms'][paymentType].items():
                offer = list(product.values())[0]
                self.assertIn('offerTermCode', offer)
