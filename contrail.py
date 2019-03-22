import argparse

from crawler import crawler
from loader import loader


def run_crawler(args):
    crawler.crawl()


def run_loader(args):
    loader.load()


def main():
    parser = argparse.ArgumentParser(description='Run one of Contrail\'s components.')

    subparsers = parser.add_subparsers(required=True)

    parser_crawler = subparsers.add_parser('crawler', aliases=['c'])
    parser_crawler.set_defaults(func=run_crawler)

    parser_loader = subparsers.add_parser('loader', aliases=['l'])
    parser_loader.set_defaults(func=run_loader)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
