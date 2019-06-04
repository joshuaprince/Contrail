import json
import unittest

from infi.clickhouse_orm.database import Database

from contrail.configuration import config
from contrail.loader.loaders.azure import AzureLoader
from contrail.loader.warehouse import InstanceData


class LoadAzureTestCase(unittest.TestCase):
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

    def test_load_file_with_capabilities(self):
        """
        Test that we can load a raw data file that has a Capabilities section.
        """
        with open('test/loader/loaders/azure/azure_limited.json', 'r') as js_file:
            data_dict = json.load(js_file)

        self._test_load_file(data_dict)

    def test_load_file_without_capabilities(self):
        """
        Test that we can load a raw data file that does not have a Capabilities section, to simulate loading files
        that were crawled before that section was added.
        """
        with open('test/loader/loaders/azure/azure_limited.json', 'r') as js_file:
            data_dict = json.load(js_file)

        data_dict.pop('Capabilities')

        self._test_load_file(data_dict)

    def _test_load_file(self, file: dict):
        """
        Helper function to the two above tests. Actually runs the test on the data specified.

        Sample file contains 7 meters: 1 is a SQL Database (not loaded), 6 are the following:
          - F2/F2s Windows Low Priority in US West 2 @ 0.0766
          - M32s Linux Low Priority (does not have a corresponding Capability info, not loaded)
          - A6 Windows in AP Southeast @ 0.64
          - F2s v2 Linux Low Priority in US West 2 @ 0.017
          - D32 v3/D32s v3 Linux Low Priority in US Central @ 0.352
          - F4/F4s Linux in US Gov AZ @ 0.239

        :param file: The file to load, as a dict. May or may not contain Capability information
        """
        AzureLoader.load(
            filename="Azure/US/2019-05-06T03:55:18.174709.json.gz",
            json=file,
            last_modified="2019-04-15T03:55:18.174709",
            db=self.test_db
        )

        # Make sure that the 'Azure' provider tag is put on each instance
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(provider='Azure').count(), 5)

        # Make sure that only the 3 instances that are meant to be loaded were loaded, and no more
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='F2/F2s').count(), 1)
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='S3 Secondary DTUs').count(), 0)
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='M32s').count(), 0)  # No capabs
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='A6 Basic').count(), 1)
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='F2s v2').count(), 1)
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='D32 v3/D32s v3').count(), 1)
        self.assertEqual(InstanceData.objects_in(self.test_db).filter(instanceType='F4/F4s').count(), 1)

        # First loaded instance: F2s v2 Low Priority in US West 2 @ 0.017
        f2s = InstanceData.objects_in(self.test_db).filter(instanceType='F2s v2')[0]  # type: InstanceData
        self.assertEqual(f2s.pricePerHour, 0.017)
        self.assertEqual(f2s.priceUpfront, 0)
        self.assertEqual(f2s.region, 'US West 2')
        self.assertEqual(f2s.priceType, 'Spot')  # Low Priority = Spot
        self.assertEqual(f2s.vcpu, 2)
        self.assertEqual(f2s.memory, 4)
        if 'Capabilities' in file:  # Only need to check Azure-specifics if the capabilities are definitely available
            self.assertEqual(f2s.maxResourceVolumeMb, 16384)
            self.assertEqual(f2s.osVhdSizeMb, 1047552)
            self.assertEqual(f2s.hyperVGenerations, 'V1,V2')
            self.assertEqual(f2s.maxDataDiskCount, 4)
            self.assertTrue(f2s.lowPriorityCapable)
            self.assertTrue(f2s.premiumIo)
            self.assertEqual(f2s.vcpusAvailable, 2)
            self.assertEqual(f2s.acus, 195)
            # There are more, but this should be sufficient in testing that these details are received

        d32 = InstanceData.objects_in(self.test_db).filter(instanceType='D32 v3/D32s v3')[0]  # type: InstanceData
        self.assertEqual(d32.pricePerHour, 0.352)
        self.assertEqual(d32.vcpu, 32)
        self.assertEqual(d32.memory, 128)
        self.assertFalse(d32.premiumIo)
