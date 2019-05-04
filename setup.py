from distutils.core import setup

setup(
    name='contrail',
    version='0.1',
    description='Public cloud market price tracker for Amazon EC2 and Azure',
    url='https://github.com/joshuaprince/Contrail',
    py_modules=[
        'crawler',
        'frontend',
        'loader'
    ],
    scripts=[
        'contrail'
    ]
)
