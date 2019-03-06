import json
import os
import collections
import itertools
import re

from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm import models, fields, engines
from clickhouse_driver import Client

class InstanceData(models.Model):
	capacityStatus = fields.NullableField(fields.StringField())
	clockSpeed = fields.NullableField(fields.StringField())
	currentGeneration = fields.NullableField(fields.StringField())
	dedicatedEbsThroughput = fields.NullableField(fields.StringField())
	ebsOptimized = fields.NullableField(fields.StringField())
	ecu = fields.NullableField(fields.StringField())
	elasticGraphicsType = fields.NullableField(fields.StringField())
	enhancedNetworkingSupported = fields.NullableField(fields.StringField())
	fromLocation = fields.NullableField(fields.StringField())
	fromLocationType = fields.NullableField(fields.StringField())
	gpu = fields.NullableField(fields.StringField())
	gpuMemory = fields.NullableField(fields.StringField())
	group = fields.NullableField(fields.StringField())
	groupDescription = fields.NullableField(fields.StringField())
	instance = fields.NullableField(fields.StringField())
	instanceCapacity10xlarge = fields.NullableField(fields.StringField())
	instanceCapacity12xlarge = fields.NullableField(fields.StringField())
	instanceCapacity16xlarge = fields.NullableField(fields.StringField())
	instanceCapacity18xlarge = fields.NullableField(fields.StringField())
	instanceCapacity24xlarge = fields.NullableField(fields.StringField())
	instanceCapacity2xlarge = fields.NullableField(fields.StringField())
	instanceCapacity32xlarge = fields.NullableField(fields.StringField())
	instanceCapacity4xlarge = fields.NullableField(fields.StringField())
	instanceCapacity8xlarge = fields.NullableField(fields.StringField())
	instanceCapacity9xlarge = fields.NullableField(fields.StringField())
	instanceCapacityLarge = fields.NullableField(fields.StringField())
	instanceCapacityMedium = fields.NullableField(fields.StringField())
	instanceCapacityXlarge = fields.NullableField(fields.StringField())
	instanceFamily = fields.NullableField(fields.StringField())
	instanceType = fields.NullableField(fields.StringField())
	instanceSKU = fields.NullableField(fields.StringField())
	intelAvx2Available = fields.NullableField(fields.StringField())
	intelAvxAvailable = fields.NullableField(fields.StringField())
	intelTurboAvailable = fields.NullableField(fields.StringField())
	licenseModel = fields.NullableField(fields.StringField())
	location = fields.NullableField(fields.StringField())
	locationType = fields.NullableField(fields.StringField())
	maxIopsBurstPerformance = fields.NullableField(fields.StringField())
	maxIopsVolume = fields.NullableField(fields.StringField())
	maxThroughputVolume = fields.NullableField(fields.StringField())
	maxVolumeSize = fields.NullableField(fields.StringField())
	memory = fields.NullableField(fields.StringField())
	networkPerformance = fields.NullableField(fields.StringField())
	normalizationSizeFactor = fields.NullableField(fields.StringField())
	operatingSystem = fields.NullableField(fields.StringField())
	operation = fields.NullableField(fields.StringField())
	physicalCores = fields.NullableField(fields.StringField())
	physicalProcessor = fields.NullableField(fields.StringField())
	preInstalledSw = fields.NullableField(fields.StringField())
	processorArchitecture = fields.NullableField(fields.StringField())
	processorFeatures = fields.NullableField(fields.StringField())
	productFamily = fields.NullableField(fields.StringField())
	provisioned = fields.NullableField(fields.StringField())
	serviceCode = fields.NullableField(fields.StringField())
	serviceName = fields.NullableField(fields.StringField())
	storage = fields.NullableField(fields.StringField())
	storageMedia = fields.NullableField(fields.StringField())
	tenancy = fields.NullableField(fields.StringField())
	toLocation = fields.NullableField(fields.StringField())
	toLocationType = fields.NullableField(fields.StringField())
	transferType = fields.NullableField(fields.StringField())
	usageType = fields.NullableField(fields.StringField())
	vcpu = fields.NullableField(fields.StringField())
	volumeType = fields.NullableField(fields.StringField())
	
	onDemandAppliesTo = fields.NullableField(fields.StringField())
	onDemandBeginRange = fields.NullableField(fields.StringField())
	onDemandCurrency = fields.NullableField(fields.StringField())
	onDemandDescription = fields.NullableField(fields.StringField())
	onDemandEffectiveDate = fields.NullableField(fields.StringField())
	onDemandEndRange = fields.NullableField(fields.StringField())
	onDemandOfferTermCode = fields.NullableField(fields.StringField())
	onDemandRateCode = fields.NullableField(fields.StringField())
	onDemandPricePerUnit = fields.NullableField(fields.StringField())
	onDemandPriceUnit = fields.NullableField(fields.StringField())

	reservedAppliesTo = fields.NullableField(fields.StringField())
	reservedBeginRange= fields.NullableField(fields.StringField())
	reservedCurrency = fields.NullableField(fields.StringField())
	reservedDescription = fields.NullableField(fields.StringField())
	reservedEffectiveDate = fields.NullableField(fields.StringField())
	reservedEndRange = fields.NullableField(fields.StringField())
	reservedLeaseContractLength = fields.NullableField(fields.StringField())
	reservedOfferTermCode = fields.NullableField(fields.StringField())
	reservedOfferingClass = fields.NullableField(fields.StringField())
	reservedPurchaseOption = fields.NullableField(fields.StringField())
	reservedRateCode = fields.NullableField(fields.StringField())
	reservedPricePerUnit = fields.NullableField(fields.StringField())
	reservedPriceUnit = fields.NullableField(fields.StringField())

	SpotPrice = fields.NullableField(fields.StringField())
	Timestamp = fields.NullableField(fields.StringField())
	InstanceType = fields.NullableField(fields.StringField())
	AvailabilityZone = fields.NullableField(fields.StringField())

	engine = engines.Memory()

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

def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, collections.abc.Mapping):
            yield from nested_dict_iter(value)
        else:
            yield key, value


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

def getData(d, mylist):
	data = {}
	for sku, details in d.items():
		values = []
		a = d.get(sku)
		for i in mylist:
			try:
				values.append((i, a[i]))
			except(KeyError, AttributeError):
				pass
		try:
			data[sku].append(values)
		except KeyError:
			data[sku] = values
	return data

def getSpotData(d, keys):
	attributes = []
	data = []
	for instance in d:
		attributes.append(instance.keys())
	attributes = sorted(set(list(itertools.chain(*attributes))))
	spot_attributes = sorted(set(attributes) - set(list(set(attributes) & set(keys))))
	attributes = keys+spot_attributes
	for instance in d:
		values = []
		for i in attributes:
			try:
				values.append((i, instance[i]))
			except(KeyError, AttributeError):
				pass
		data.append(values)
	return data

def load():
	'''
	Loads data from local JSON files into database
	TODO: Load data from s3 buckets
	'''
	db = Database('contrail')
	db.create_table(InstanceData)
	fil = open('../tmp.json')
	fil2 = open('../spot_data.json')
	d2 = json.load(fil2)
	d = json.load(fil, object_pairs_hook=collections.OrderedDict)
	product_dict, on_demand_dict, reserved_dict, product_keys, on_demand_keys, reserved_keys = getAllAttributes(d)
	spot_data = getSpotData(d2, product_keys + on_demand_keys + reserved_keys)
	product_attribute_data = getData(product_dict, product_keys)
	on_demand_data = getData(on_demand_dict, on_demand_keys)
	reserved_data = getData(reserved_dict, reserved_keys)
	data = {key: product_attribute_data[key.split('.')[0]] + on_demand_data[key.split('.')[0]] + value for key, value in reserved_data.items()}
	items = list(data.values()) + spot_data

	for item in items:
		instance = InstanceData()
		for i in item:
			setattr(instance, i[0], str(i[1]))
		db.insert([instance])

if __name__ == '__main__':
	load()