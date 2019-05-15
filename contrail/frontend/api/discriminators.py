discriminators = {
    'AmazonEC2': [
        'instanceType',
        'region',
        'operatingSystem'
    ],
    'Azure': [
        'instanceType',
        'region',
        'operatingSystem'
    ]
}

conditions = {
    'AmazonEC2': {
        'instanceSKU': [None],
        'productFamily': ['Compute Instance', 'Compute Instance (bare metal)', '', None],
        'tenancy': ['Shared'],
        'preInstalledSw': ['NA']
    }
}
