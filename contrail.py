import argparse
import os
import sys

from crawler import crawler
from loader import loader


def run_crawler(args):
    crawler.crawl()


def run_loader(args):
    loader.load()


def run_frontend(args):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.contrails.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv[1:])


def main():
    parser = argparse.ArgumentParser(description='Run one of Contrail\'s components.')

    subparsers = parser.add_subparsers(required=True, dest="component")

    parser_crawler = subparsers.add_parser('crawler', aliases=['c'])
    parser_crawler.set_defaults(func=run_crawler)

    parser_loader = subparsers.add_parser('loader', aliases=['l'])
    parser_loader.set_defaults(func=run_loader)

    parser_frontend = subparsers.add_parser('frontend', aliases=['f', 'manage.py', 'manage', 'm'])
    parser_frontend.set_defaults(func=run_frontend)

    args, unknown = parser.parse_known_args()
    args.func(args)


if __name__ == '__main__':
    main()
