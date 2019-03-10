# Contrail

## Public Cloud Market Price Tracker

### UC Davis ECS 193, 2019


## Development
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



## API
`/api/getinstances/`
Given attributes, return instances that match and their prices
