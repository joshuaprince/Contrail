# Contrail

### Public Cloud Market Price Tracker

### UC Davis ECS 193, 2019
Contrail is a public cloud market price tracker that allows you to easily access and compare the prices and
characteristics of VMs over various locations, cloud providers, and times.

## Quick Start
### Virtual Environment
Create virtual environment:
```
virtualenv -p python3 venv
OR
python3 -m virtualenv venv
```

Start virtual environment:
```
source venv/bin/activate
```

You should see `(venv)` show up in command prompt.

Install requirements our project uses:
```
pip install -r requirements.txt
```

To exit virtual environment:
```
deactivate
```


### Start Django
Make sure you are in the main Contrail folder and the virtual environment is activated.

Collect static files and set up the database:
```
python contrail.py frontend collectstatic
python contrail.py frontend makemigrations
python contrail.py frontend migrate
```

Start the Django server:
```
python contrail.py frontend runserver
```

Open [127.0.0.1:8000](http://127.0.0.1:8000) in a browser.


## API
`/api/getinstances/`\
Given attributes, return instances that match and their prices\
request:
```
{
    'operating_system': "Linux",
    'aws': "True",
    'gcp': "True",
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


## Collecting your own data
Contrail is split into a few distinct components:
- Crawler: Collects and stores raw offer data from various cloud providers.
- Loader: Parses raw offer data and stores it in a Clickhouse data warehouse.
- API/Frontend: Communicates with the data warehouse and displays data nicely.
 
The Quick Start above only sets up the API/Frontend component. By default, it points to our own data source. You will
have to set up your own backend (crawler and loader) to collect your own data.

Read more about setting up the first two components here:
[Crawler](/crawler/README.md),
[Loader](/loader/README.md).
