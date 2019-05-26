import logging
from typing import Dict, List

from contrail.crawler.providers.azure import Azure
from contrail.loader.loaders import BaseLoader, register_loader
from contrail.loader.warehouse import InstanceData

logger = logging.getLogger('contrail.loader.azure')


@register_loader(provider=Azure)
class AzureLoader(BaseLoader):
    _stand_in_capabilities = {}

    @classmethod
    def get_stand_in_capabilities(cls) -> Dict[str, Dict]:
        """
        Raw files crawled in earlier versions of Contrail do not have a Capabilities section from which we can get
        instance data such as vCPUs, memory, etc. We load and cache a current version of the Capabilities mapping so
        that these instances have these mappings that is most likely accurate.
        TODO: This functionality can be eliminated once all raw data has capability data embedded.
        """
        if not cls._stand_in_capabilities:
            cls._stand_in_capabilities = Azure().request_capabilities()

        return cls._stand_in_capabilities

    @classmethod
    def should_load(cls, meter: dict) -> bool:
        """
        Determine if this Meter should be loaded into the database, filtering out:
          - Non-VMs
          - Compute Hours
          - Windows machines
          - Expired meters
          - Instances that don't specify a region (?)
        """
        # Load VM instances only
        if meter['MeterCategory'] != 'Virtual Machines':
            return False

        # Don't load "compute hours", which are not actually VMs
        if meter['MeterName'] == 'Compute Hours':
            return False

        # Don't load expired meters
        if 'Expired' in meter['MeterName']:
            return False

        # Strangely, some meters just don't specify a region. Skip those too
        if not meter['MeterRegion']:
            return False

        return True

    @classmethod
    def normalize_meter_name(cls, meter_name: str) -> (str, str, bool):
        """
        Azure "instance sizes" are stored in the raw data in the MeterName field. This field contains the name of the
        instance size (i.e. M32s) but also might say "Low Priority" to designate this offer as a spot-like instance.
        Also, it may reflect the pricing of multiple similar instance types, such as "F2/F2s".

        Examples:
          - "M32s Low Priority" -> ("M32s", "M32s", True)
          - "F2/F2s Low Priority" -> ("F2/F2s", "F2", True)
          - "A6" -> ("A6", "A6", False)

        :return: A tuple consisting of the instance's size(s) (i.e. F2/F2s), the key to get its capabilities (i.e. F2),
        and a bool that is True if this is a Low Priority instance or false otherwise.
        """
        lp = ' Low Priority'
        is_spot = False

        if meter_name.endswith(lp):
            meter_name = meter_name[:-len(lp)]
            is_spot = True

        capability_key = meter_name.split('/')[0]

        return meter_name, capability_key, is_spot

    @classmethod
    def normalize(cls, meter: dict, all_capabilities: dict) -> InstanceData or None:
        """
        Convert a meter dict to an InstanceData object.
        """
        inst = InstanceData()

        inst.provider = 'Azure'
        inst.meterId = meter['MeterId']
        inst.region = meter['MeterRegion']
        inst.pricePerHour = meter['MeterRates']['0']

        size, capability_key, is_spot = cls.normalize_meter_name(meter['MeterName'])
        inst.instanceType = size
        if 'Basic' in meter['MeterSubCategory']:
            inst.instanceType += ' Basic'
        inst.priceType = ('Spot' if is_spot else 'On Demand')

        inst.operatingSystem = 'Windows' if 'Windows' in meter['MeterSubCategory'] else 'Linux'

        capabilities = all_capabilities.get(capability_key)
        if not capabilities:
            # Not all instance sizes seem to have a corresponding capabilities lookup.
            # For now, just don't load these instances (this makes up ~3% of all instances, all of them are M or N type)
            # logger.warning("Couldn't get capabilities for instance size {} ({})".format(size, meter['MeterId']))
            return None

        inst.vcpu = capabilities['vCPUs']
        inst.memory = capabilities['MemoryGB']
        inst.gpu = capabilities.get('GPUs', 0)

        # Azure-specific fields. Not required, so we use get() instead of [] so there aren't any errors if unspecified
        inst.meterSubCategory = meter['MeterSubCategory']
        inst.maxResourceVolumeMb = capabilities.get('MaxResourceVolumeMB')
        inst.osVhdSizeMb = capabilities.get('OSVhdSizeMB')
        inst.hyperVGenerations = capabilities.get('HyperVGenerations')
        inst.maxDataDiskCount = capabilities.get('MaxDataDiskCount')
        inst.lowPriorityCapable = capabilities.get('LowPriorityCapable')
        inst.premiumIo = capabilities.get('PremiumIO')
        inst.vcpusAvailable = capabilities.get('vCPUsAvailable')
        inst.vcpusPerCore = capabilities.get('vCPUsPerCore')
        inst.ephemeralOsDiskSupported = capabilities.get('EphemeralOSDiskSupported')
        inst.acus = capabilities.get('ACUs')
        inst.combinedTempDiskAndCachedReadBytesPerSecond = capabilities.get('CombinedTempDiskAndCachedReadBytesPerSecond')
        inst.combinedTempDiskAndCachedWriteBytesPerSecond = capabilities.get('CombinedTempDiskAndCachedWriteBytesPerSecond')
        inst.combinedTempDiskAndCachedIOPS = capabilities.get('CombinedTempDiskAndCachedIOPS')
        inst.uncachedDiskBytesPerSecond = capabilities.get('UncachedDiskBytesPerSecond')
        inst.uncachedDiskIOPS = capabilities.get('UncachedDiskIOPS')
        inst.cachedDiskBytes = capabilities.get('CachedDiskBytes')
        inst.maxWriteAcceleratorDisksAllowed = capabilities.get('MaxWriteAcceleratorDisksAllowed')

        return inst

    @classmethod
    def load(cls, filename: str, json: dict, last_modified: str, db):
        logger.info("Loading file {} into ClickHouse.".format(filename.split('/')[-1]))

        # If this file contains capability data, use that. Fall back on stand-in data
        all_capabilities = json.get('Capabilities') or cls.get_stand_in_capabilities()

        instances = []  # type: List[InstanceData]

        for meter in json['Meters']:
            if not cls.should_load(meter):
                continue

            inst = cls.normalize(meter, all_capabilities)
            if not inst:
                continue
            inst.crawlTime = last_modified
            instances.append(inst)

        # Insert rows 1000 rows at a time
        insertables = [instances[i * 1000:(i + 1) * 1000] for i in range((len(instances) + 1000 - 1) // 1000 )]
        for inst in insertables:
            db.insert(inst)
