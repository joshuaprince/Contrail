# Contrail

### Public Cloud Market Price Tracker

### UC Davis ECS 193, 2019
Contrail is a public cloud market price tracker that allows you to easily access and compare the prices and characteristics of VMs over various locations and cloud providers.

## Quick Start
### virtual env
create virtual environment
```
virtual env -p python3 venv
OR
python3 -m virtualenv venv
```

start virtual environment
```
source venv/bin/activate
```

should see `(venv)` show up in command prompt

install requirements our project uses
```
pip install -r requirements.txt
```


to exit virtual environment
```
deactivate
```


### start Django
```
python manage.py runserver
```
open [127.0.0.1:8000](127.0.0.1:8000)

set up database (do this whenever changes made to model)
```
python manage.py makemigrations
python manage.py migrate
```
#### Admin
username: admin\
password: pw

## To set up backend
Click the links to go visit documentation\
[Crawler](/crawler/README.md)


## API
`/api/getinstances/`\
Given attributes, return instances that match and their prices\
request:
```
{
    'operating_system': "Linux",
    'aws': "True",
    'gcp': "True"],
    'azure': "False",
    'region': None,
    'vcpus': None,
    'memory': 8,
}
```
response:
```
{
    "instance_type": "c4"
    "operating_system": "Linux",
    "provider": "AWS",
    "region": "US East",
    "vcpus": 8,
    "memory": 8,
    "reserved", "spot",
    "price_type": "on_demand",
    "price": 0.233,
    "price_unit": "per hour"
}
```
