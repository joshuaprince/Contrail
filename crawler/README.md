# Contrail Crawler

This module retrieves data at a fixed interval for a number of cloud service providers. It compresses and uploads this raw data into a "Data Lake" architecture, backed by Amazon's S3 service.

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

3. Obtain credentials for an S3 instance and set up a bucket. 

4. **Create a file called** `secret.py` in the root Contrail directory. Its format should be as follows, replacing the X's with data about your AWS credentials and the name of the bucket to upload data:

    ```python
    AWS_ACCESS_KEY_ID = 'XXXXXXXXXXXXXXXXXXXX'
    AWS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
    AWS_BUCKET_NAME = 'XXXXXXXXXXX'
    ```

## Usage

1. Ensure that the virtual environment is active:

    ```shell
    source venv/bin/activate
    ``` 

2. Run `crawler.py`. The crawler will run until it is stopped with `^C`.
