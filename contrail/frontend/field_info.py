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
    'friendlyName': 'VCPUs',
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
