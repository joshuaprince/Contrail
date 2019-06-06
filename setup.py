import setuptools

with open('README.md', 'r') as readme_file:
    long_description = readme_file.read()

setuptools.setup(
    name='contrail',
    version='1.0.0',
    description='Public cloud market price tracker for Amazon EC2 and Azure',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/joshuaprince/Contrail',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django :: 2.2",
        "Intended Audience :: System Administrators",
    ],
    entry_points={
        'console_scripts': [
            'contrail = contrail.main:main'
        ]
    },
    install_requires=[
        'boto3',
        'cachetools',
        'Django < 3',
        'django-crispy-forms',
        'infi.clickhouse_orm',
        'requests'
    ],
)
