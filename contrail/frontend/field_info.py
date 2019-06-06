"""
This file contains a mapping from a database column name to its friendly name, and an optional description of what the
field describes.

Allowed field options:
  - friendlyName: The name that will be displayed in place of the unformatted column name.
  - hint: Help text that describes what this field means. Typically used as hover text.
  - unit: The unit that will be appended to any value displayed.
  - exclude: If true, this field will not be displayed.
"""
from collections import OrderedDict

FIELD_INFO = OrderedDict()

# Universal fields -------------------------------------------------------------
FIELD_INFO['provider'] = {
    'friendlyName': 'Provider',
}

FIELD_INFO['region'] = {
    'friendlyName': 'Region',
}

FIELD_INFO['instanceType'] = {
    'friendlyName': 'Instance Type',
}

FIELD_INFO['operatingSystem'] = {
    'friendlyName': 'Operating System',
}

FIELD_INFO['vcpu'] = {
    'friendlyName': 'vCPUs',
    'hint': 'Number of Virtual CPUs allotted to this instance.'
}

FIELD_INFO['memory'] = {
    'friendlyName': 'Memory',
    'unit': 'GB'
}

FIELD_INFO['gpu'] = {
    'friendlyName': 'GPUs',
    'hint': 'Number of Graphics Processing Units allotted to this instance.'
}

FIELD_INFO['clockSpeed'] = {
    'friendlyName': 'Clock Speed',
    'unit': 'GHz'
}

# EC2 specific -----------------------------------------------------------------
FIELD_INFO['enhancedNetworkingSupported'] = {
    'friendlyName': 'Enhanced Networking Support',
    'link': 'https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/enhanced-networking.html'
}

FIELD_INFO['sku'] = {
    'friendlyName': 'SKU',
    'hint': 'A unique serial number for this instance.'
}

FIELD_INFO['clockSpeedIsUpTo'] = {
    'friendlyName': 'Clock Speed Is Up To',
}

FIELD_INFO['currentGeneration'] = {
    'friendlyName': 'Current Generation',
}

FIELD_INFO['dedicatedEbsThroughputIsUpTo'] = {
    'friendlyName': 'Dedicated EBS Throughput Is Up To',
}

FIELD_INFO['dedicatedEbsThroughput'] = {
    'friendlyName': 'Dedicated EBS Throughput',
}

FIELD_INFO['ecu Is Variable'] = {
    'friendlyName': 'ECU Is Variable',
}

FIELD_INFO['licenseModel'] = {
    'friendlyName': 'License Model',
}

FIELD_INFO['location'] = {
    'friendlyName': 'Location',
}

FIELD_INFO['locationType'] = {
    'friendlyName': 'Location Type',
}

FIELD_INFO['nerworkPerformance'] = {
    'friendlyName': 'Network Performance',
}

FIELD_INFO['normalizationSizeFactor'] = {
    'friendlyName': 'Normalization Size Factor',
    'link': 'https://aws.amazon.com/blogs/aws/new-instance-size-flexibility-for-ec2-reserved-instances/'
}

FIELD_INFO['operation'] = {
    'friendlyName': 'Operation',
}

FIELD_INFO['physicalProcessor'] = {
    'friendlyName': 'Physical Processor',
}

FIELD_INFO['preInstalledSw'] = {
    'friendlyName': 'Preinstalled Software',
}

FIELD_INFO['processorArchitecture'] = {
    'friendlyName': 'Processor Architecture',
}

FIELD_INFO['productFamily'] = {
    'friendlyName': 'Product Family',
}

FIELD_INFO['serviceName'] = {
    'friendlyName': 'Service Name',
}

FIELD_INFO['storageIsEbsOnly'] = {
    'friendlyName': 'Storage Is EBS Only',
}

FIELD_INFO['usageType'] = {
    'friendlyName': 'Usage Type',
    'link': 'https://aws.amazon.com/about-aws/whats-new/2016/09/new-filtering-options-for-aws-cost-explorer/'
}

FIELD_INFO['ecuIsVariable'] = {
    'friendlyName': 'ECU Is Variable',
}

FIELD_INFO['networkPerformance'] = {
    'friendlyName': 'Network Performance',
}

FIELD_INFO['processorFeatures'] = {
    'friendlyName': 'Processor Features',
}

FIELD_INFO['storageCount'] = {
    'friendlyName': 'Storage Count',
}

FIELD_INFO['storageCapacity'] = {
    'friendlyName': 'Storage Capacity',
}

FIELD_INFO['storageType'] = {
    'friendlyName': 'Storage Type',
}

FIELD_INFO['storageClass'] = {
    'friendlyName': 'Storage Class',
}

FIELD_INFO['offeringClass'] = {
    'friendlyName': 'Offering Class',
}

for field in ['capacityStatus', 'effectiveDate', 'beginRange', 'endRange', 'tenancy', 'appliesTo', 'description']:
    FIELD_INFO[field] = {'exclude': True}

# Azure specific ---------------------------------------------------------------
FIELD_INFO['instanceFamily'] = {
    'friendlyName': 'Instance Family',
}

FIELD_INFO['vcpusAvailable'] = {
    'friendlyName': 'VCPUs Available',
}

FIELD_INFO['vcpusPerCore'] = {
    'friendlyName': 'VCPUs per Core',
}

FIELD_INFO['meterId'] = {
    'exclude': True
}

FIELD_INFO['meterSubCategory'] = {
    'friendlyName': 'Meter Sub Category',
}

FIELD_INFO['maxResourceVolumeMb'] = {
    'friendlyName': 'Max Resource Volume',
    'unit': 'MB'
}

FIELD_INFO['osVhdSizeMb'] = {
    'friendlyName': 'OS VHD Size',
    'unit': 'MB'
}

FIELD_INFO['hyperVGenerations'] = {
    'friendlyName': 'Hyper V Generations',
}

FIELD_INFO['maxDataDiskCount'] = {
    'friendlyName': 'Max Data Disk Count',
}

FIELD_INFO['lowPriorityCapable'] = {
    'friendlyName': 'Low Priority Capable',
}

FIELD_INFO['premiumIo'] = {
    'friendlyName': 'Premium IO',
}

FIELD_INFO['ephemeralOsDiskSupported'] = {
    'friendlyName': 'Ephemeral OS Disk Supported',
}

FIELD_INFO['combinedTempDiskAndCachedReadBytesPerSecond'] = {
    'friendlyName': 'Combined Temp Disk And Cached Read Bytes Per Second',
}

FIELD_INFO['combinedTempDiskAndCachedWriteBytesPerSecond'] = {
    'friendlyName': 'Combined Temp Disk And Cached Write Bytes Per Second',
}

FIELD_INFO['combinedTempDiskAndCachedIOPS'] = {
    'friendlyName': 'Combined Temp Disk And Cached IOPS',
}

FIELD_INFO['uncachedDiskBytesPerSecond'] = {
    'friendlyName': 'Uncached Disk Bytes Per Second',
}

FIELD_INFO['uncachedDiskIOPS'] = {
    'friendlyName': 'Uncached Disk IOPS',
}

FIELD_INFO['cachedDiskBytes'] = {
    'friendlyName': 'Cached Disk Bytes',
}

FIELD_INFO['maxWriteAcceleratorDisksAllowed'] = {
    'friendlyName': 'Max Write Accelerator Disks Allowed',
}

FIELD_INFO['availabilityZone'] = {
    'friendlyName': 'Available Zone',
}

FIELD_INFO['acus'] = {
    'friendlyName': 'ACUs',
}

FIELD_INFO['ecu'] = {
    'friendlyName': 'ECU',
    'hint': 'EC2 Compute Unit - Integer processing power of an Amazon EC2 instance.'
}
