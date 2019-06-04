import datetime
import json
import logging
from typing import List, Dict

import requests
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from contrail.configuration import config
from contrail.crawler.providers import BaseProvider, register_provider

logger = logging.getLogger('contrail.crawler.azure')

URL_TOKEN_REQUEST = 'https://login.microsoftonline.com/{tenant}/oauth2/token'
"""
URL queried to obtain an Azure management access token. Replaces {tenant} with a tenant (directory) ID.
"""

URL_RATECARD_REQUEST = "https://management.azure.com:443/subscriptions/{subscriptionId}/providers/" \
                       "Microsoft.Commerce/RateCard?api-version=2016-08-31-preview&$filter=" \
                       "OfferDurableId eq 'MS-AZR-0003P' and Currency eq 'USD' " \
                       "and Locale eq 'en-US' and RegionInfo eq 'US'"
"""
URL queried to list prices. Replaces {subscriptionId}.
"""

URL_CAPABILITIES_REQUEST = "https://management.azure.com/subscriptions/{subscriptionId}/" \
                           "providers/Microsoft.Compute/skus?api-version=2017-09-01"
"""
URL queried to get instance capabilities (mapping from size to vcpus, memory, etc). Replaces {subscriptionId}.
"""


@register_provider
class Azure(BaseProvider):
    def __init__(self):
        super().__init__()
        self._access_token = ''
        self._access_token_expire = 0

    @classmethod
    def create_providers(cls) -> List['Azure']:
        return [cls()]

    def crawl(self) -> datetime.timedelta:
        ratecard = self.request_ratecard()
        ratecard['Capabilities'] = self.request_capabilities()

        self.store_provider_data(region='US', data=ratecard)

        return datetime.timedelta(minutes=60)

    def request_ratecard(self):
        url = URL_RATECARD_REQUEST.format(subscriptionId=config['AZURE']['subscription_id'])
        response = requests.get(url, allow_redirects=False,
                                headers={'Authorization': 'Bearer {}'.format(self.access_token())})

        # Initial request forces a redirect. Look at response headers to get the redirect URL
        redirect_url = response.headers['Location']

        # Get the ratecard content by making another call to go the redirect URL
        rate_card = requests.get(redirect_url)

        return json.loads(rate_card.content.decode('utf-8'))

    def request_capabilities(self) -> Dict[str, Dict]:
        """
        Get a mapping from instance sizes to parameters such as vcpus, memory, etc.
        """
        url = URL_CAPABILITIES_REQUEST.format(subscriptionId=config['AZURE']['subscription_id'])
        response = requests.get(url, allow_redirects=False,
                                headers={'Authorization': 'Bearer {}'.format(self.access_token())})

        resp_dict = json.loads(response.content.decode('utf-8'))

        capabilities = {}

        for instance in resp_dict['value']:
            if instance.get('resourceType') != 'virtualMachines':
                continue

            if instance.get('size') in capabilities:
                # Response contains each instance size multiple times, so don't load if we've already loaded this size
                continue

            size = instance['size'].replace('_', ' ')

            # Response lists capabilities like this: [{"name": "vCPUS", "value": 2}, {"name": "memory", "value": 8}...]
            # Convert it to a more pythonic form, like {"vCPUS": 2, "memory": 8...}
            capabilities[size] = {}
            for capability in instance['capabilities']:
                capabilities[size][capability['name']] = capability['value']

        return capabilities

    def _renew_access_token(self):
        """
        Retrieve an access token needed to pull pricing data.
        :return: The access token.
        """
        logger.info("Renewing access token.")

        post_data = {
            'client_id': config['AZURE']['client_id'],
            'grant_type': 'client_credentials',
            'client_secret': config['AZURE']['client_secret'],
            'resource': 'https://management.azure.com/'
        }

        request = Request(URL_TOKEN_REQUEST.format(tenant=config['AZURE']['tenant_id']), urlencode(post_data).encode())
        response = urlopen(request).read().decode()
        resp_json = json.loads(response)

        self._access_token = resp_json['access_token']
        self._access_token_expire = int(resp_json['expires_on'])

    def access_token(self) -> str:
        """
        Get a current Access token, renewing it if it is due to expire soon.
        :return:
        """
        # Renew access token 1 minute before the current one expires
        if self._access_token_expire < time.time() + 60:
            self._renew_access_token()

        return self._access_token
