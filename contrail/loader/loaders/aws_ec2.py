import collections
import itertools
import logging

from infi.clickhouse_orm.database import Database

from contrail.crawler.providers.aws_ec2 import AmazonEC2
from contrail.loader.warehouse import InstanceData
from contrail.loader.loaders import BaseLoader, register_loader
from contrail.loader.normalizers import normalizeData

logger = logging.getLogger('contrail.loader.aws_ec2')


def nested_dict_iter(nested):
    lower = lambda s: s[:1].lower() + s[1:] if s else ''
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield lower(key), value

def reserved_nested_dict_iter(nested):
    lower = lambda s: s[:1].lower() + s[1:] if s else ''
    for key, value in nested.items():
        if key != 'priceDimensions':
            if isinstance(value, collections.abc.Mapping):
                yield from nested_dict_iter(value)
            else:
                yield lower(key), value

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
            on_demand_data = dict(nested_dict_iter(a))
            on_demand_data_list = list(nested_dict_iter(a))
        except(KeyError, AttributeError):
            on_demand_data = {}
            on_demand_data_list = []
        
        try:
            for key, value in b.items():
                reserved_price_dimensions = {}
                offer_info = dict(reserved_nested_dict_iter(value))
                for i, j in value.items():
                    if i == 'priceDimensions':
                        reserved_price_dimensions = {}
                        for x in list(nested_dict_iter(j)):
                            if x[0] == 'unit' or x[0] == 'uSD' or x[0] == 'beginRange' or x[0] == 'endRange':                         
                                pd_key = x[0]
                                pd_val = x[1]
                                if 'unit' in reserved_price_dimensions and reserved_price_dimensions['unit'] == 'Quantity' and pd_key == 'uSD':
                                    reserved_price_dimensions['priceUpfront'] = pd_val
                                elif 'unit' in reserved_price_dimensions and reserved_price_dimensions['unit'] == 'Hrs' and pd_key == 'uSD':
                                    reserved_price_dimensions['pricePerHour'] = pd_val
                                else:
                                    reserved_price_dimensions[pd_key] = pd_val
                    if reserved_price_dimensions:
                        reserved_dict[key] = {**reserved_price_dimensions, **offer_info}
            reserved_data_list = list(nested_dict_iter(b)) + [('priceUpfront', ''), ('pricePerHour', '')]
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

def getData(d, mylist):
    data = {}
    for sku, details in d.items():
        filter_out = False
        values = []
        a = d.get(sku)
        for i in mylist:
            try:
                try:
                    if normalizeData(i, a[i]) == None:
                        filter_out = True
                    else:
                        key, value = normalizeData(i, a[i])
                except(ValueError):
                    values.extend(normalizeData(i, a[i]))
                    pass
                if isinstance(value, tuple):
                    values.extend((key, value))
                else:
                    values.append((key, value))
            except(KeyError, AttributeError):
                pass
        if filter_out == False:
            try:
                data[sku].append(values)
            except KeyError:
                data[sku] = values
    return data

@register_loader(provider=AmazonEC2)
class AmazonEC2Loader(BaseLoader):
    @classmethod
    def load(cls, filename: str, json: dict, last_modified: str, db: Database):
        logger.info("Loading {} into ClickHouse.".format(filename.split('/')[-1]))
        region = "{}".format(filename.split('/')[1])
        k, v = normalizeData('region', region)
        product_dict, on_demand_dict, reserved_dict, product_keys, on_demand_keys, reserved_keys = getAllAttributes(json)
        product_attribute_data = getData(product_dict, product_keys)
        on_demand_data = getData(on_demand_dict, on_demand_keys)
        reserved_data = getData(reserved_dict, reserved_keys)
        
        for key, value in on_demand_data.items():
            try:
                on_demand_data[key] = value + product_attribute_data[key] + [('priceType', 'On Demand'), ('crawlTime', last_modified), (k, v)]
            except(KeyError):
                on_demand_data[key] = []
        
        for key, value in reserved_data.items():
            try:
                reserved_data[key] = value + product_attribute_data[key[0:key.find('.')]] + [('priceType', 'Reserved'), ('crawlTime', last_modified), (k, v)]
            except(KeyError):
                reserved_data[key] = []

        items = list(on_demand_data.values()) + list(reserved_data.values())
        instances = []
        for item in items:
            if item != []:
                instance = InstanceData()
                for i in item:
                    setattr(instance, i[0], i[1])
                instances.append(instance)
        insertables = [instances[i * 1000:(i + 1) * 1000] for i in range((len(instances) + 1000 - 1) // 1000 )] 
        for inst in insertables:
            db.insert(inst)
