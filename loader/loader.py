import json
import os
<<<<<<< HEAD
import collections
from collections import abc
import itertools
import re

=======
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm import models, fields, engines
from clickhouse_driver import Client

class InstanceData(models.Model):
<<<<<<< HEAD
	capacityStatus = fields.NullableField(fields.StringField(default="None"))
	clockSpeed = fields.NullableField(fields.StringField(default="None"))
	currentGeneration = fields.NullableField(fields.StringField(default="None"))
	dedicatedEbsThroughput = fields.NullableField(fields.StringField(default="None"))
	ebsOptimized = fields.NullableField(fields.StringField(default="None"))
	ecu = fields.NullableField(fields.StringField(default="None"))
	elasticGraphicsType = fields.NullableField(fields.StringField(default="None"))
	enhancedNetworkingSupported = fields.NullableField(fields.StringField(default="None"))
	fromLocation = fields.NullableField(fields.StringField(default="None"))
	fromLocationType = fields.NullableField(fields.StringField(default="None"))
	gpu = fields.NullableField(fields.StringField(default="None"))
	gpuMemory = fields.NullableField(fields.StringField(default="None"))
	group = fields.NullableField(fields.StringField(default="None"))
	groupDescription = fields.NullableField(fields.StringField(default="None"))
	instance = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity10xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity12xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity16xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity18xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity24xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity2xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity32xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity4xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity8xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacity9xlarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacityLarge = fields.NullableField(fields.StringField(default="None"))
	instanceCapacityMedium = fields.NullableField(fields.StringField(default="None"))
	instanceCapacityXlarge = fields.NullableField(fields.StringField(default="None"))
	instanceFamily = fields.NullableField(fields.StringField(default="None"))
	instanceType = fields.NullableField(fields.StringField(default="None"))
	instanceSKU = fields.NullableField(fields.StringField(default="None"))
	intelAvx2Available = fields.NullableField(fields.StringField(default="None"))
	intelAvxAvailable = fields.NullableField(fields.StringField(default="None"))
	intelTurboAvailable = fields.NullableField(fields.StringField(default="None"))
	licenseModel = fields.NullableField(fields.StringField(default="None"))
	location = fields.NullableField(fields.StringField(default="None"))
	locationType = fields.NullableField(fields.StringField(default="None"))
	maxIopsBurstPerformance = fields.NullableField(fields.StringField(default="None"))
	maxIopsVolume = fields.NullableField(fields.StringField(default="None"))
	maxThroughputVolume = fields.NullableField(fields.StringField(default="None"))
	maxVolumeSize = fields.NullableField(fields.StringField(default="None"))
	memory = fields.NullableField(fields.StringField(default="None"))
	networkPerformance = fields.NullableField(fields.StringField(default="None"))
	normalizationSizeFactor = fields.NullableField(fields.StringField(default="None"))
	operatingSystem = fields.NullableField(fields.StringField(default="None"))
	operation = fields.NullableField(fields.StringField(default="None"))
	physicalCores = fields.NullableField(fields.StringField(default="None"))
	physicalProcessor = fields.NullableField(fields.StringField(default="None"))
	preInstalledSw = fields.NullableField(fields.StringField(default="None"))
	processorArchitecture = fields.NullableField(fields.StringField(default="None"))
	processorFeatures = fields.NullableField(fields.StringField(default="None"))
	productFamily = fields.NullableField(fields.StringField(default="None"))
	provisioned = fields.NullableField(fields.StringField(default="None"))
	serviceCode = fields.NullableField(fields.StringField(default="None"))
	serviceName = fields.NullableField(fields.StringField(default="None"))
	storage = fields.NullableField(fields.StringField(default="None"))
	storageMedia = fields.NullableField(fields.StringField(default="None"))
	tenancy = fields.NullableField(fields.StringField(default="None"))
	toLocation = fields.NullableField(fields.StringField(default="None"))
	toLocationType = fields.NullableField(fields.StringField(default="None"))
	transferType = fields.NullableField(fields.StringField(default="None"))
	usageType = fields.NullableField(fields.StringField(default="None"))
	vcpu = fields.NullableField(fields.StringField(default="None"))
	volumeType = fields.NullableField(fields.StringField(default="None"))
	
	onDemandAppliesTo = fields.NullableField(fields.StringField(default="None"))
	onDemandBeginRange = fields.NullableField(fields.StringField(default="None"))
	onDemandCurrency = fields.NullableField(fields.StringField(default="None"))
	onDemandDescription = fields.NullableField(fields.StringField(default="None"))
	onDemandEffectiveDate = fields.NullableField(fields.StringField(default="None"))
	onDemandEndRange = fields.NullableField(fields.StringField(default="None"))
	onDemandOfferTermCode = fields.NullableField(fields.StringField(default="None"))
	onDemandRateCode = fields.NullableField(fields.StringField(default="None"))
	onDemandPricePerUnit = fields.NullableField(fields.StringField(default="None"))
	onDemandPriceUnit = fields.NullableField(fields.StringField(default="None"))

	reservedAppliesTo = fields.NullableField(fields.StringField(default="None"))
	reservedBeginRange= fields.NullableField(fields.StringField(default="None"))
	reservedCurrency = fields.NullableField(fields.StringField(default="None"))
	reservedDescription = fields.NullableField(fields.StringField(default="None"))
	reservedEffectiveDate = fields.NullableField(fields.StringField(default="None"))
	reservedEndRange = fields.NullableField(fields.StringField(default="None"))
	reservedLeaseContractLength = fields.NullableField(fields.StringField(default="None"))
	reservedOfferTermCode = fields.NullableField(fields.StringField(default="None"))
	reservedOfferingClass = fields.NullableField(fields.StringField(default="None"))
	reservedPurchaseOption = fields.NullableField(fields.StringField(default="None"))
	reservedRateCode = fields.NullableField(fields.StringField(default="None"))
	reservedPricePerUnit = fields.NullableField(fields.StringField(default="None"))
	reservedPriceUnit = fields.NullableField(fields.StringField(default="None"))

	spotPrice = fields.NullableField(fields.StringField(default="None"))
	spotInstanceType = fields.NullableField(fields.StringField(default="None"))
	spotProductDescription = fields.NullableField(fields.StringField(default="None"))
	spotTimeStamp = fields.NullableField(fields.StringField(default="None"))
	spotAvailabilityZone = fields.NullableField(fields.StringField(default="None"))

	engine = engines.Memory()

def reserved_nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
            yield from reserved_nested_dict_iter(value)
        else:
            yield 'reserved' + re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1), value

def on_demand_nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
            yield from on_demand_nested_dict_iter(value)
        else:
            yield 'onDemand' + re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), key, 1), value

def nested_dict_iter(nested):
    for key, value in nested.items():
        if isinstance(value, abc.Mapping):
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
				values.append(a[i])
			except(KeyError, AttributeError):
				values.append(None)
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
				values.append(instance[i])
			except(KeyError, AttributeError):
				values.append(None)
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
	data = {key: product_attribute_data[key.split('.')[0]] + on_demand_data[key.split('.')[0]] + value + [None]*5 for key, value in reserved_data.items()}
	items = list(data.values()) + spot_data
	for lst in items:
		i = InstanceData(
			capacityStatus=lst[0],
			clockSpeed=lst[1],
			currentGeneration=lst[2],
			dedicatedEbsThroughput=lst[3],
			ebsOptimized=lst[4],
			ecu=lst[5],
			elasticGraphicsType=lst[6],
			enhancedNetworkingSupported=lst[7],
			fromLocation=lst[8],
			fromLocationType=lst[9],
			gpu=lst[10],
			gpuMemory=lst[11],
			group=lst[12],
			groupDescription=lst[13],
			instance=lst[14],
			instanceCapacity10xlarge=lst[15],
			instanceCapacity12xlarge=lst[16],
			instanceCapacity16xlarge=lst[17],
			instanceCapacity18xlarge=lst[18],
			instanceCapacity24xlarge=lst[19],
			instanceCapacity2xlarge=lst[20],
			instanceCapacity32xlarge=lst[21],
			instanceCapacity4xlarge=lst[22],
			instanceCapacity8xlarge=lst[23],
			instanceCapacity9xlarge=lst[24],
			instanceCapacityLarge=lst[25],
			instanceCapacityMedium=lst[26],
			instanceCapacityXlarge=lst[27],
			instanceFamily=lst[28],
			instanceType=lst[29],
			instanceSKU=lst[30],
			intelAvx2Available=lst[31],
			intelAvxAvailable=lst[32],
			intelTurboAvailable=lst[33],
			licenseModel=lst[34],
			location=lst[35],
			locationType=lst[36],
			maxIopsBurstPerformance=lst[37],
			maxIopsVolume=lst[38],
			maxThroughputVolume=lst[39],
			maxVolumeSize=lst[40],
			memory=lst[41],
			networkPerformance=lst[42],
			normalizationSizeFactor=lst[43],
			operatingSystem=lst[44],
			operation=lst[45],
			physicalCores=lst[46],
			physicalProcessor=lst[47],
			preInstalledSw=lst[48],
			processorArchitecture=lst[49],
			processorFeatures=lst[50],
			productFamily=lst[51],
			provisioned=lst[52],
			serviceCode=lst[53],
			serviceName=lst[54],
			storage=lst[56],
			storageMedia=lst[57],
			tenancy=lst[58],
			toLocation=lst[59],
			toLocationType=lst[60],
			transferType=lst[61],
			usageType=lst[62],
			vcpu=lst[63],
			volumeType=lst[64],

			onDemandAppliesTo=str(lst[65]),
			onDemandBeginRange=lst[66],
			onDemandCurrency='USD',
			onDemandDescription=lst[67],
			onDemandEffectiveDate=lst[68],
			onDemandEndRange=lst[69],
			onDemandOfferTermCode=lst[70],
			onDemandRateCode=lst[71],
			onDemandPricePerUnit=lst[73],
			onDemandPriceUnit=lst[74],

			reservedAppliesTo=str(lst[75]),
			reservedBeginRange=lst[76],
			reservedDescription=lst[77],
			reservedEffectiveDate=lst[78],
			reservedEndRange=lst[79],
			reservedLeaseContractLength=lst[80],
			reservedOfferTermCode=lst[81],
			reservedOfferingClass=lst[82],
			reservedPurchaseOption=lst[83],
			reservedRateCode=lst[84],
			reservedPricePerUnit=lst[86],
			reservedPriceUnit=lst[87],

			spotAvailabilityZone = lst[88],
			spotInstanceType = lst[89],
			spotProductDescription = lst[90],
			spotPrice = lst[91],
			spotTimeStamp = lst[92]

		)
		db.insert([i])

load()
=======
	serviceCode = fields.NullableField(fields.StringField(default="None"))
	location = fields.NullableField(fields.StringField(default="None"))
	locationType = fields.NullableField(fields.StringField(default="None"))
	instanceType = fields.NullableField(fields.StringField(default="None"))
	currentGeneration = fields.NullableField(fields.StringField(default="None"))
	instanceFamily = fields.NullableField(fields.StringField(default="None"))
	vcpu = fields.NullableField(fields.StringField(default="None"))
	processor = fields.NullableField(fields.StringField(default="None"))
	clockSpeed = fields.NullableField(fields.StringField(default="None"))
	memory = fields.NullableField(fields.StringField(default="None"))
	storage = fields.NullableField(fields.StringField(default="None"))
	networkPerformance = fields.NullableField(fields.StringField(default="None"))
	processorArchitecture = fields.NullableField(fields.StringField(default="None"))
	tenancy = fields.NullableField(fields.StringField(default="None"))
	operatingSystem = fields.NullableField(fields.StringField(default="None"))
	licenseModel = fields.NullableField(fields.StringField(default="None"))
	usageType = fields.NullableField(fields.StringField(default="None"))
	operation = fields.NullableField(fields.StringField(default="None"))
	capacityStatus = fields.NullableField(fields.StringField(default="None"))
	dedicatedEbsThroughput = fields.NullableField(fields.StringField(default="None"))
	ecu = fields.NullableField(fields.StringField(default="None"))
	enhancedNetworkingSupported = fields.NullableField(fields.StringField(default="None"))
	instanceSKU = fields.NullableField(fields.StringField(default="None"))
	normalizationSizeFactor = fields.NullableField(fields.StringField(default="None"))
	preInstalledSw = fields.NullableField(fields.StringField(default="None"))
	processorFeatures = fields.NullableField(fields.StringField(default="None"))
	termType = fields.NullableField(fields.StringField(default="None"))
	effectiveDate = fields.NullableField(fields.StringField(default="None"))
	rateCode = fields.NullableField(fields.StringField(default="None"))
	description = fields.NullableField(fields.StringField(default="None"))
	endRange = fields.NullableField(fields.StringField(default="None"))
	unit = fields.NullableField(fields.StringField(default="None"))
	currency = fields.NullableField(fields.StringField(default="None"))
	pricePerUnit = fields.NullableField(fields.StringField(default="None"))

	engine = engines.MergeTree('effectiveDate', ('instanceType', 'termType', 'effectiveDate'))

db = Database('my_test_db')
db.create_table(InstanceData)

fil = open('../tmp.json')
d = json.load(fil)

output = {}

for sku, product in d['products'].items():
	instanceType = product['attributes'].get('instanceType')
	vcpu = product['attributes'].get('vcpu')
	processor = product['attributes'].get('physicalProcessor')
	location = product['attributes'].get('location')
	clockSpeed = product['attributes'].get('clockSpeed')
	memory = product['attributes'].get('memory')
	storage = product['attributes'].get('storage')
	networkPerformance = product['attributes'].get('networkPerformance')
	processorArchitecture = product['attributes'].get('processorArchitecture')
	operatingSystem = product['attributes'].get('operatingSystem')

	try:
		a = d['terms']['OnDemand'].get(sku)
		b = next(iter(a.values()))['priceDimensions']
		unit = next(iter(b.values()))['unit']
	except(KeyError, AttributeError):
		unit = None

	try:
		a = d['terms']['OnDemand'].get(sku)
		b = next(iter(a.values()))['priceDimensions']
		c = next(iter(b.values()))['pricePerUnit']
		pricePerUnit = next(iter(c.values()))
	except(KeyError, AttributeError):
		pricePerUnit = None

	try:
		output[sku].append(sku, instanceType, vcpu, processor, location, clockSpeed, memory, storage, networkPerformance, processorArchitecture, operatingSystem, unit, pricePerUnit)
	except KeyError:
		output[sku] = [sku, instanceType, vcpu, processor, location, clockSpeed, memory, storage, networkPerformance, processorArchitecture, operatingSystem, unit, pricePerUnit]


# for size, lst in output.items():
# 	instance = InstanceData(
# 		service='Amazon', 
# 		instanceType=lst[1],
# 		vcpu=lst[2],
# 		processor=lst[3],
# 		location=lst[4],
# 		clockSpeed=lst[5],
# 		memory=lst[6],
# 		storage=lst[7],
# 		networkPerformance=lst[8],
# 		processorArchitecture=lst[9],
# 		operatingSystem=lst[10],
# 		termType='OnDemand',
# 		unit=lst[11],
# 		pricePerUnit=lst[12]
# 	)
# 	db.insert([instance])
>>>>>>> db07c504d65da152d645da995264d947f8d15cf9
