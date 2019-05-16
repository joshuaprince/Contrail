discriminators = {
    'AmazonEC2': [
        'provider',
        'instanceType',
        'region',
    #    'operatingSystem'
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
