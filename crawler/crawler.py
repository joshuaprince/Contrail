<<<<<<< HEAD
import asyncio
import datetime
import logging
import sys

from crawler.providers.aws_ec2 import AmazonEC2
from crawler.providers.aws_ec2_spot import AmazonEC2Spot

logger = logging.getLogger('contrail.crawler')
=======
import logging
from time import sleep

from crawler.providers.aws_ec2 import AmazonEC2

DEFAULT_CRAWL_PERIOD_S = 5
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9

providers = []


def register_provider(instance):
    """
    Register a provider class with the crawler to ensure this provider is crawled.
    """
    providers.append(instance)


def load_providers() -> int:
    """
    Loads all modules in the `providers` directory.
    :return: The number of providers loaded.
    """
    # TODO Make this dynamically load all modules in providers/
<<<<<<< HEAD
    provider_count = 0

    register_provider(AmazonEC2())
    provider_count += 1

    AmazonEC2Spot.load_instance_type_details()
    spot_rgns = AmazonEC2Spot.create_providers()
    for p in spot_rgns:
        register_provider(p)
    provider_count += len(spot_rgns)

    return provider_count


async def _crawl_loop(provider):
    while True:
        time_wait: datetime.timedelta = provider.crawl() or datetime.timedelta(minutes=1)
        await asyncio.sleep(time_wait.total_seconds())


async def _dummy_loop():
    # A task to keep the event loop doing something even when it has nothing else to do, so that keyboard interrupts
    # don't appear to hang until something comes through the loop.
    # TODO fix this workaround
    while True:
        await asyncio.sleep(1)


async def _main():
    provider_tasks = [_crawl_loop(p) for p in providers]
    provider_tasks.append(_dummy_loop())
    await asyncio.gather(*provider_tasks)


def crawl():
    """
    Runs the crawler until a keyboard interrupt is received.
    """
    logging.basicConfig(
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    logger.info("Starting crawler.")

    try:
        num_providers = load_providers()
        logger.info("Loaded {} providers.".format(num_providers))

        asyncio.run(_main())
    except KeyboardInterrupt:
        print("Crawler is shutting down.")


if __name__ == '__main__':
    crawl()
=======
    register_provider(AmazonEC2())
    return 1


def crawl(period: int = DEFAULT_CRAWL_PERIOD_S):
    """
    Runs the crawler until an interrupt is received.
    :param period: Number of seconds to wait between data requests.
    """
    logging.info("Starting crawler.")
    num_providers = load_providers()
    logging.info("Loaded {} providers.".format(num_providers))

    # Loop crawler until interrupted
    # TODO Ensure fairness between providers in this loop
    try:
        while True:
            for p in providers:
                p.crawl()
                sleep(period)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    crawl()
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
