import datetime
import unittest

from contrail.crawler.providers import REGISTERED_PROVIDER_CLASSES, import_provider_directory, BaseProvider, register_provider


class BaseProviderTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_register_provider(self):
        """
        Test the @register_provider decorator.
        """
        @register_provider
        class TestProvider(BaseProvider):
            @classmethod
            def create_providers(cls):
                return [cls()]

            @classmethod
            def provider_name(cls):
                return "Test Provider"

            def crawl(self):
                return datetime.timedelta(seconds=5)

        self.assertIn(TestProvider, REGISTERED_PROVIDER_CLASSES,
                      "@register_provider failed to add a class to REGISTERED_PROVIDER_CLASSES.")

    def test_import_provider_directory(self):
        """
        Test that we can import the provider directory, and that it discovers at least one provider.
        """
        import_provider_directory()

        self.assertTrue(len(REGISTERED_PROVIDER_CLASSES) > 0,
                        "Failed to register any provider classes. The crawler won't do anything.")

    def test_all_providers_extend_base(self):
        """
        Test that all registered providers extend from BaseProvider.
        """
        import_provider_directory()

        for provider in REGISTERED_PROVIDER_CLASSES:
            self.assertTrue(issubclass(provider, BaseProvider),
                            "All classes decorated with @register_provider must inherit from BaseProvider.")

