#!/usr/bin/env python3
import argparse
import os
import sys

try:
    import config
except ImportError:
    print("Couldn't load config.py. Make a copy of config_example.py and see the README to configure Contrail.")
    sys.exit(1)


def run_crawler(args):
    from contrail.crawler import crawler
    crawler.crawl()


def run_loader(args):
    from contrail.loader import loader
    loader.load()


def run_frontend(args):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contrail.frontend.contrails.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv[1:])


def run_tests(args):
    import unittest
    suite = unittest.TestLoader().discover('test', top_level_dir='.')
    unittest.TextTestRunner().run(suite)


def main():
    parser = argparse.ArgumentParser(description='Run one of Contrail\'s components.')

    subparsers = parser.add_subparsers(dest="component")
    subparsers.required = True

    parser_crawler = subparsers.add_parser('crawler', aliases=['c'])
    parser_crawler.set_defaults(func=run_crawler)

    parser_loader = subparsers.add_parser('loader', aliases=['l'])
    parser_loader.set_defaults(func=run_loader)

    parser_frontend = subparsers.add_parser('frontend', aliases=['f', 'manage.py', 'manage', 'm'])
    parser_frontend.set_defaults(func=run_frontend)

    parser_test = subparsers.add_parser('test', aliases=['t'])
    parser_test.set_defaults(func=run_tests)

    args, unknown = parser.parse_known_args()
    args.func(args)


if __name__ == '__main__':
    main()
