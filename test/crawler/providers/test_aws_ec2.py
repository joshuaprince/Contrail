import json
import unittest

import requests

from contrail.crawler.providers.aws_ec2 import AmazonEC2, URL_REGION_VERSION


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
        try:
            self.instance.load_regions()

            # Get the us-west-1 region to test on
            region = self.instance.get_next_region()
            while region['regionCode'] != 'us-west-1':
                self.assertTrue(self.instance.region_queued(), "Couldn't find region 'us-west-1'.")
                region = self.instance.get_next_region()

            region_url_postfix = region['currentVersionUrl']

            response_obj = requests.get(URL_REGION_VERSION.format(currentVersionUrl=region_url_postfix))
            response_json = response_obj.content.decode('utf-8')
            response_dict = json.loads(response_json)

            self.assertEqual(response_dict['formatVersion'], 'v1.0', "formatVersion mismatch: at /formatVersion")
            self.assertEqual(response_dict['offerCode'], 'AmazonEC2', "offerCode mismatch: at /offerCode")
            self.assertIn('version', response_dict, "version missing: at /version")

            self.assertIn('products', response_dict, "products list missing: at /products/")
            for name, product in response_dict['products'].items():
                if product['productFamily'] == 'Data Transfer':
                    # For now, ignore data transfer products, which are not compute instances and don't match format
                    continue

                self.assertIn('sku', product, "sku missing: at /products/{0}/sku".format(name))
                self.assertIn('attributes', product, "attributes missing: at /products/{0}/attributes/".format(name))
                self.assertIn('location', product['attributes'],
                              "location missing: at /products/{0}/attributes/location".format(name))

            self.assertIn('terms', response_dict, "terms missing: at /terms/")

            for paymentType in ('OnDemand', 'Reserved'):
                self.assertIn(paymentType, response_dict['terms'], "{0} missing: at /terms/{0}/".format(paymentType))
                for name, product in response_dict['terms'][paymentType].items():
                    offer = list(product.values())[0]
                    self.assertIn('offerTermCode', offer,
                                  "offerTermCode missing: at /terms/{0}/{1}/offerTermCode/".format(paymentType, name))

        except AssertionError:
            with open('ec2_erroneous.json', 'w') as outfile:
                json.dump(response_dict, outfile, indent=2)

            print("Encountered a structural error with the JSON retrieved from AWS.")
            print("Writing the erroneous data to 'ec2_erroneous.json'")
            print("The location of the error within the JSON hierarchy can be found in the error message below.")

            raise
