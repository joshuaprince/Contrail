import configparser
import os
from collections import OrderedDict

CFG_LOCATION = os.path.expanduser(os.path.join('~', '.contrail'))
CFG_NAME = 'contrail.ini'
CFG_FILE = os.path.join(CFG_LOCATION, CFG_NAME)

config = configparser.ConfigParser()

# Build config defaults --------------------------------------------------------
config['CLICKHOUSE'] = OrderedDict()
config['CLICKHOUSE']['db_url'] = 'http://contrail.tk:8123'
config['CLICKHOUSE']['db_name'] = 'contrail'

config['AWS'] = OrderedDict()
config['AWS']['access_key_id'] = ''
config['AWS']['secret'] = ''
config['AWS']['bucket_name'] = ''

config['AZURE'] = OrderedDict()
config['AZURE']['client_id'] = ''
config['AZURE']['client_secret'] = ''
config['AZURE']['tenant_id'] = ''
config['AZURE']['subscription_id'] = ''

config['WEBSITE'] = OrderedDict()
config['WEBSITE']['secret_key'] = '3_k9to*4cdxdu8d^uuu@xox5gn$2t6va+exit$kwyhob(4klg#'
config['WEBSITE']['allowed_hosts'] = 'localhost,127.0.0.1,contrail.tk'
config['WEBSITE']['debug'] = 'false'
# End config defaults ----------------------------------------------------------

config.read(CFG_FILE)

if not os.path.exists(CFG_LOCATION):
    os.mkdir(CFG_LOCATION)

with open(CFG_FILE, 'w') as outfile:
    outfile.writelines(["; This is Contrail's configuration file. For information about what the settings\n",
                        "; mean, please see https://github.com/joshuaprince/Contrail\n\n"], )
    config.write(outfile)
