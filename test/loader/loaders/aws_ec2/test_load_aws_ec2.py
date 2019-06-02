import json
import unittest
from typing import List

from infi.clickhouse_orm.database import Database

from contrail.configuration import config
from contrail.loader.loaders.aws_ec2 import AmazonEC2Loader
from contrail.loader.warehouse import InstanceData


class LoadAmazonEC2TestCase(unittest.TestCase):
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
            - 1 product ('VG6Z') with no instanceSKU
            - 2 On Demand terms; one for G5FF, one for VG6Z
            - 12 Reserved terms for VG6Z
            - All instances share the same hardware and software configurations
        """

        with open('test/loader/loaders/aws_ec2/ec2_limited.json', 'r') as js_file:
            data_dict = json.load(js_file)

        AmazonEC2Loader.load(
            filename="AmazonEC2/ap-northeast-1/2019-04-15T03:55:18.174709.json.gz",
            json=data_dict,
            last_modified="2019-04-15T03:55:18.174709",
            db=self.test_db
        )

        instances = list(InstanceData.objects_in(self.test_db))  # type: List[InstanceData]

        self.assertEqual(len(instances), 13)  # 1 on demand + 12 reserved

        # Check for correct hardware/software parameters common to all offers
        for inst in instances:
            self.assertEqual(inst.instanceType, 'c4.4xlarge')
            self.assertEqual(inst.operatingSystem, 'Linux')
            self.assertEqual(inst.vcpu, 16)
            self.assertEqual(inst.clockSpeed, 2.9)
            self.assertEqual(inst.memory, 30)

        # Check for several different pricing types to be loaded correctly

        # On Demand price
        self.assertTrue(any(inst.pricePerHour == 2.928 for inst in instances))

        # Reserved price: all up front
        self.assertTrue(any(inst.priceUpfront == 63106 and inst.leaseContractLength == '3yr' for inst in instances))
        self.assertTrue(any(inst.priceUpfront == 22726 and inst.leaseContractLength == '1yr' for inst in instances))

        # Reserved price: half up front/half hourly
        self.assertTrue(any(inst.priceUpfront == 32966 and inst.pricePerHour == 1.254 for inst in instances))

        # Reserved price: all hourly
        self.assertTrue(any(inst.pricePerHour == 2.751 for inst in instances))
