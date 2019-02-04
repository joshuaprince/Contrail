import logging
from time import sleep

from crawler.providers.aws_ec2 import AmazonEC2

CRAWL_PERIOD_S = 5

providers = []


def register_provider(instance):
    """
    Register a provider class with the crawler to ensure this provider is crawled.
    """
    providers.append(instance)


def load_providers():
    """
    Loads all modules in the `providers` directory.
    """
    # TODO Make this dynamically load all modules in providers/
    logging.info("Loading providers")
    register_provider(AmazonEC2())


if __name__ == '__main__':
    load_providers()

    # TODO Ensure fairness between providers in this loop
    while True:
        for p in providers:
            p.crawl()
            sleep(CRAWL_PERIOD_S)
