import unittest
import unittest.mock
import copyingmock

from contrail.crawler.providers.aws_ec2_spot import AmazonEC2Spot


class AmazonEC2SpotTestCase(unittest.TestCase):
    def setUp(self):
        self.instances = AmazonEC2Spot.create_providers()

    def test_crawl(self):
        """
        Check that some number of crawl iterations result in uploading data to S3.
        """
        mocked_instance = self.instances[0]
        mocked_instance.store_provider_data = copyingmock.CopyingMock()

        # The crawl procedure may take several iterations before attempting to upload data.
        #   Continue calling crawl() until it does call store_provider_data().
        while not mocked_instance.store_provider_data.called:
            mocked_instance.crawl()

        uploaded_data = mocked_instance.store_provider_data.call_args[1]['data']

        # Check that at least one instance was found
        self.assertGreater(len(uploaded_data), 0)

        # Check for common fields on each instance
        for instance in uploaded_data:
            self.assertIn('InstanceType', instance)
            self.assertIn('SpotPrice', instance)
            self.assertIn('vcpu', instance)
            self.assertIn('memory', instance)
            self.assertIn('Timestamp', instance)

    def test_load_instance_type_details(self):
        """
        Ensure that we can load details about instance types (i.e. a mapping between 't2.xlarge' -> 2 vcpus, etc.)
        """
        instance_types = AmazonEC2Spot.get_instance_type_details()

        # Make sure that one (arbitrarily selected) instance type can be indexed in this details dict
        self.assertIn('m3.large', instance_types)

        # Make sure that each instance type's value contains some general information about that instance type
        for instance_type in iter(instance_types.values()):
            self.assertIn('instanceType', instance_type)
            self.assertIn('vcpu', instance_type)
            self.assertIn('memory', instance_type)
            self.assertIn('storage', instance_type)
