import collections
import itertools
import re

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