import asyncio
import datetime
import logging
import sys
from typing import List

from contrail.crawler.providers import BaseProvider, REGISTERED_PROVIDER_CLASSES, import_provider_directory

logger = logging.getLogger('contrail.crawler')

providers = []  # type: List[BaseProvider]


async def _crawl_loop(provider: BaseProvider):
    """
    Endlessly crawls over a single provider, yielding between successive crawls.
    :param provider:
    :return:
    """
    while True:
        # noinspection PyBroadException
        try:
            time_wait = provider.crawl()  # type: datetime.timedelta
        except Exception:
            # If a crawl attempt had an error, print error and try again in 2 minutes
            logger.exception("Caught exception while crawling {provider}".format(provider=provider.provider_name()))
            logger.info("Cooling down for 2 minutes before retry.")
            time_wait = datetime.timedelta(minutes=2)

        await asyncio.sleep(time_wait.total_seconds())


async def _dummy_loop():
    # A task to keep the event loop doing something even when it has nothing else to do, so that keyboard interrupts
    # don't appear to hang until something comes through the loop.
    # TODO fix this workaround
    while True:
        await asyncio.sleep(1)


async def _main():
    """
    Main async loop for the crawler.
    """
    provider_tasks = [_crawl_loop(p) for p in providers]
    provider_tasks.append(_dummy_loop())
    await asyncio.gather(*provider_tasks)


def create_providers():
    """
    Imports all providers in the crawler/providers directory, and loads them into `providers`
    """
    import_provider_directory()
    for provider_class in REGISTERED_PROVIDER_CLASSES:
        providers.extend(provider_class.create_providers())


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

    create_providers()
    logger.info("Loaded {} providers from {} provider classes.".format(len(providers), len(REGISTERED_PROVIDER_CLASSES)))

    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(_main())
    except KeyboardInterrupt:
        print("Crawler is shutting down.")


if __name__ == '__main__':
    crawl()
