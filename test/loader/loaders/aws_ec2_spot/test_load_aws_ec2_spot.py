import json
import unittest
from typing import List

from infi.clickhouse_orm.database import Database

from contrail.configuration import config
from contrail.loader.loaders.aws_ec2_spot import AmazonEC2SpotLoader
from contrail.loader.warehouse import InstanceData


class LoadAmazonEC2SpotTestCase(unittest.TestCase):
    def setUp(self):
        self.test_db = Database(db_name='contrail_test', db_url=config['CLICKHOUSE']['db_url'])

        # Make sure we have a clean database to test on
        if self.test_db.db_exists:
            self.test_db.drop_database()

        self.test_db.create_database()
        self.test_db.create_table(InstanceData)

    def tearDown(self):
        self.test_db.drop_database()
        pass

    def test_load_file(self):
        """
        Basic tests loading the sample file.

        Sample file is formatted to the following specs:
            - 10 instances total from eu-west-3 region, various availability zones within
            - Instance types: 1x m5d.12xlarge, 1x c5.2xlarge, 3x t3.nano, 5x c5d.4xlarge
            - VCPUs, memory, spot price, timestamp specified for all
            - Clock speeds omitted for t3.nano types
        """

        with open('test/loader/loaders/aws_ec2_spot/ec2_spot_limited.json', 'r') as js_file:
            data_dict = json.load(js_file)

        AmazonEC2SpotLoader.load(
            filename="AmazonEC2Spot/eu-west-3/2019-04-28T22:34:47.158605.json.gz",
            json=data_dict,
            last_modified="2019-04-28T22:34:47.158605",
            db=self.test_db
        )

        instances = list(InstanceData.objects_in(self.test_db))  # type: List[InstanceData]

        self.assertEqual(len(instances), 10)

        # Check for no upfront prices on each, since spot instances never have up front pricing
        for inst in instances:
            self.assertFalse(inst.priceUpfront)  # price == 0 or None

        # Check that explicit instances were loaded
        m5d12xl = next(i for i in instances if i.instanceType == 'm5d.12xlarge')
        self.assertEqual(m5d12xl.ecu, 173)
        self.assertEqual(m5d12xl.vcpu, 48)
        self.assertEqual(m5d12xl.memory, 192)
        self.assertEqual(m5d12xl.clockSpeed, 2.5)
        self.assertEqual(m5d12xl.pricePerHour, 0.9523)
        self.assertEqual(m5d12xl.operatingSystem, 'Linux')

        c52xl = next(i for i in instances if i.instanceType == 'c5.2xlarge')
        self.assertEqual(c52xl.ecu, 34)
        self.assertEqual(c52xl.vcpu, 8)
        self.assertEqual(c52xl.memory, 16)
        self.assertEqual(c52xl.clockSpeed, 3.0)
        self.assertEqual(c52xl.pricePerHour, 0.1298)
        self.assertEqual(c52xl.operatingSystem, 'Windows')

        for i in instances:
            if not i.instanceType == 't3.nano':
                continue
            self.assertEqual(i.memory, 0.5)
            self.assertEqual(i.vcpu, 2)
            self.assertFalse(i.clockSpeed)  # clock speed is unspecified for t3.nano instances in raw data
            self.assertEqual(i.pricePerHour, 0.0059)
