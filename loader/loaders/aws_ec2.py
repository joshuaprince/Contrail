import collections
import itertools
import logging
import re

from crawler.providers.aws_ec2 import AmazonEC2
from loader.warehouse import InstanceData, db
from loader.loaders import BaseLoader, register_loader
from loader.normalizers import getData

logger = logging.getLogger('contrail.loader.aws_ec2')


def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield key, value

def reserved_nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from reserved_nested_dict_iter(value)
        else:
            yield 'reserved' + re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1), value

def on_demand_nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from on_demand_nested_dict_iter(value)
        else:
            yield 'onDemand' + re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1), value

def getAllAttributes(d):
    product_dict = {}
    on_demand_dict = {}
    reserved_dict = {}
    product_keys = []
    on_demand_keys = []
    reserved_keys = []
    for sku, product in d['products'].items():
        a = d['terms']['OnDemand'].get(sku)
        b = d['terms']['Reserved'].get(sku)
        try:
            product_attributes = dict(nested_dict_iter(product))
            product_attributes_list = list(nested_dict_iter(product))
        except(KeyError, AttributeError):
            product_attributes = {}
            product_attributes_list = []
        try:
            on_demand_data = dict(on_demand_nested_dict_iter(a))
            on_demand_data_list = list(on_demand_nested_dict_iter(a))
        except(KeyError, AttributeError):
            on_demand_data = {}
            on_demand_data_list = []
        try:
            reserved_data_list = list(reserved_nested_dict_iter(b))
            for key, value in b.items():
                reserved_data = dict(reserved_nested_dict_iter(value))
                try:
                    reserved_dict[key].append(reserved_data)
                except(KeyError, AttributeError):
                    reserved_dict[key] = reserved_data
            reserved_keys.append([i[0] for i in reserved_data_list])
        except(KeyError, AttributeError):
            reserved_data = {}
        product_keys.append([i[0] for i in product_attributes_list])
        on_demand_keys.append([i[0] for i in on_demand_data_list])
        try:
            product_dict[sku].append(product_attributes)
            on_demand_dict[sku].append(on_demand_data)
        except(KeyError, AttributeError):
            product_dict[sku] = product_attributes
            on_demand_dict[sku] = on_demand_data
    product_keys = sorted(set(list(itertools.chain(*product_keys))))
    on_demand_keys = sorted(set(list(itertools.chain(*on_demand_keys))))
    reserved_keys = sorted(set(list(itertools.chain(*reserved_keys))))
    return product_dict, on_demand_dict, reserved_dict, product_keys, on_demand_keys, reserved_keys


@register_loader(provider=AmazonEC2)
class AmazonEC2Loader(BaseLoader):
    @classmethod
    def load(cls, filename: str, json: dict):
        logger.info("Loading {} into ClickHouse.".format(filename.split('/')[-1]))
        product_dict, on_demand_dict, reserved_dict, product_keys, on_demand_keys, reserved_keys = getAllAttributes(json)
        product_attribute_data = getData(product_dict, product_keys)
        on_demand_data = getData(on_demand_dict, on_demand_keys)
        reserved_data = getData(reserved_dict, reserved_keys)
        combineddata = {key: on_demand_data[key] + value for key, value in product_attribute_data.items()}
        data = {}
        lst = []
        for key, value in combineddata.items():
            for k, v in reserved_data.items():
                if k.startswith(key):
                    lst.append(key)
                    try:
                        data[k].append(value + v)
                    except(KeyError):
                        data[k] = value + v
            if key not in set(lst):
                try:
                    data[key].append(value)
                except(KeyError):
                    data[key] = value

        items = list(data.values())  # + spot_data
        for item in items:
            instance = InstanceData()
            for i in item:
                setattr(instance, i[0], i[1])
            db.insert([instance])
