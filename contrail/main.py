#!/usr/bin/env python3
import argparse
import os
import sys

from contrail.configuration import config, CFG_FILE


def check_config(*required_sections):
    for section in required_sections:
        for key in config[section]:
            if not config[section][key]:
                print("Couldn't find required configuration setting '{}'. Please set one in {}".format(key, CFG_FILE))
                exit(1)


def run_crawler(args):
    check_config('AWS', 'AZURE')
    from contrail.crawler import crawler
    crawler.crawl()


def run_loader(args):
    check_config('AWS', 'CLICKHOUSE')
    from contrail.loader import loader
    loader.load()


def run_initdb(args):
    from contrail.loader.warehouse import create_contrail_table
    create_contrail_table(True)


def run_fixdb(args):
    from contrail.loader.warehouse import fix_aggregated_data
    fix_aggregated_data()


def run_frontend(args):
    check_config('CLICKHOUSE', 'WEBSITE')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contrail.frontend.settings.settings')
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
    print("Starting CONTRAIL with configuration file {}".format(CFG_FILE))
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

    parser_init = subparsers.add_parser('initdb')
    parser_init.set_defaults(func=run_initdb)

    parser_fix = subparsers.add_parser('fixdb')
    parser_fix.set_defaults(func=run_fixdb)

    args, unknown = parser.parse_known_args()
    args.func(args)


if __name__ == '__main__':
    main()
