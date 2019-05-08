# Contrail Loader

This module loads data from S3 bucket and inserts it into the ClickHouse database. 

## Setup

1. Create and activate a Python virtual environment in the main Contrail directory:

    ```shell
    virtualenv venv
    source venv/bin/activate
    ``` 

2. Install prerequisites:

    ```shell
    pip install -r requirements.txt
    ```
3. Follow https://clickhouse.yandex/#quick-start to install ClickHouse and get the server running locally


## Usage

1. Ensure that the virtual environment is active:

    ```shell
    source venv/bin/activate
    ``` 

2. Run `python contrail.py loader`. 

3. Run the following commands to launch the command-line client to query into the database:

    ```shell
    clickhouse-client
    use contrail
    ```
