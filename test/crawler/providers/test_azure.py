import unittest
import unittest.mock

from contrail.crawler.providers.azure import Azure


class AzureTestCase(unittest.TestCase):
    def setUp(self):
        self.instance = Azure.create_providers()[0]

    def test_get_access_token(self):
        """
        Check that we can successfully retrieve a bearer token from Azure's servers.
        """
        token = self.instance.access_token()

        # A valid bearer token consists of a Header, Payload, and Signature, separated by periods.
        # Basic checks that the token looks approximately correct.
        self.assertEqual(token.count('.'), 2)
        self.assertGreater(len(token), 5)

    def test_get_ratecard(self):
        """
        Check that we can use the bearer token to retrieve a RateCard response.
        """
        ratecard = self.instance.request_ratecard()

        # Structural checks for raw ratecard response
        self.assertIn('OfferTerms', ratecard)
        self.assertIn('Meters', ratecard)
        self.assertEqual(ratecard['Currency'], 'USD')
        self.assertEqual(ratecard['Locale'], 'en-US')

        # Ensure at least 1 offer has come back.
        self.assertGreater(len(ratecard['Meters']), 0)

        # Structural checks for each ratecard offer
        for meter in ratecard['Meters']:
            self.assertIn('EffectiveDate', meter)
            self.assertIn('MeterRates', meter)
            self.assertIn('MeterRegion', meter)

    def test_crawl(self):
        """
        Check that the crawl function properly attempts to upload raw data to S3.
        """
        # Create a mocked instance of an Azure provider. In this mocked instance, we replace S3 upload functionality
        #   with our own "mock" function and ensure that it has been called.
        mocked_instance = Azure.create_providers()[0]
        mocked_instance.store_provider_data = unittest.mock.MagicMock()

        mocked_instance.crawl()

        # Make sure that the crawl has attempted to upload exactly once.
        self.assertEqual(mocked_instance.store_provider_data.call_count, 1)

        # Make sure that this crawl most likely attempted to upload real data, by ensuring that it called upload with
        #   data that contains a 'Meters' key.
        self.assertIn('Meters', mocked_instance.store_provider_data.call_args[1]['data'])
