# This is an example configuration file for Contrail.
# Copy it to `config.py` and fill in all of these fields with your own keys.
# See `crawler/README.md` for details about how to get your own keys for these services.

CLICKHOUSE_DB_URL = 'http://localhost:8123'
CLICKHOUSE_DB_NAME = 'contrail'

AWS_ACCESS_KEY_ID = ''
AWS_SECRET = ''
AWS_BUCKET_NAME = ''

AZURE_CLIENT_ID = ''
AZURE_CLIENT_SECRET = ''
AZURE_TENANT_ID = ''
AZURE_SUBSCRIPTION_ID = ''

# Settings for the Contrail Django frontend website.
FRONTEND_SECRET_KEY = '3_k9to*4cdxdu8d^uuu@xox5gn$2t6va+exit$kwyhob(4klg#'
FRONTEND_ALLOWED_HOSTS = []  # e.g. 'contrail.mysite.com'
FRONTEND_DEBUG = False  # Debug mode - leave False in production
