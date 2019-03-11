import json
import os
import re
import itertools

from loader.providers.load_aws_ec2 import getAllAttributes
from loader.providers.load_aws_ec2_spot import getSpotData

from infi.clickhouse_orm.database import Database
from infi.clickhouse_orm.fields import Field
from infi.clickhouse_orm import models, fields, engines
from clickhouse_driver import Client

class BooleanField(Field):

    # The ClickHouse column type to use
    db_type = 'UInt8'

    # The default value
    class_default = False

    def to_python(self, value, timezone_in_use):
        # Convert valid values to bool
        if value in (1, '1', True, 'True', 'Yes'):
            return True
        elif value in (0, '0', False, 'False', 'No'):
            return False
        else:
            raise ValueError('Invalid value for BooleanField: %r' % value)

    def to_db_string(self, value, quote=True):
        # The value was already converted by to_python, so it's a bool
        return '1' if value else '0'

class InstanceData(models.Model):
	capacityStatus = fields.NullableField(fields.StringField())
	clockSpeedIsUpTo = fields.NullableField(BooleanField())
	clockSpeed = fields.NullableField(fields.Float32Field()) #in GHz
	currentGeneration = fields.NullableField(BooleanField())
	dedicatedEbsThroughputIsUpTo = fields.NullableField(BooleanField())
	dedicatedEbsThroughput = fields.NullableField(fields.Int32Field()) #in Mbps
	ebsOptimized = fields.NullableField(BooleanField())
	ecuIsVariable = fields.NullableField(BooleanField())
	ecu = fields.NullableField(fields.Float32Field())
	elasticGraphicsType = fields.NullableField(fields.StringField())
	enhancedNetworkingSupported = fields.NullableField(BooleanField())
	fromLocation = fields.NullableField(fields.StringField())
	fromLocationType = fields.NullableField(fields.StringField())
	gpu = fields.NullableField(fields.Int32Field())
	gpuMemory = fields.NullableField(fields.StringField())
	group = fields.NullableField(fields.StringField())
	groupDescription = fields.NullableField(fields.StringField())
	instance = fields.NullableField(fields.StringField())
	instanceCapacity10xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity12xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity16xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity18xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity24xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity2xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity32xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity4xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity8xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacity9xlarge = fields.NullableField(fields.Int32Field())
	instanceCapacityLarge = fields.NullableField(fields.Int32Field())
	instanceCapacityMedium = fields.NullableField(fields.Int32Field())
	instanceCapacityXlarge = fields.NullableField(fields.Int32Field())
	instanceFamily = fields.NullableField(fields.StringField())
	instanceType = fields.NullableField(fields.StringField())
	instanceSKU = fields.NullableField(fields.StringField())
	intelAvx2Available = fields.NullableField(BooleanField())
	intelAvxAvailable = fields.NullableField(BooleanField())
	intelTurboAvailable = fields.NullableField(BooleanField())
	licenseModel = fields.NullableField(fields.StringField())
	location = fields.NullableField(fields.StringField())
	locationType = fields.NullableField(fields.StringField())
	maxIopsBurstPerformance = fields.NullableField(fields.StringField())
	maxIopsVolume = fields.NullableField(fields.StringField())
	maxThroughputVolume = fields.NullableField(fields.StringField())
	maxVolumeSize = fields.NullableField(fields.Int32Field()) #in TiB
	memory = fields.NullableField(fields.Float32Field()) #in GiB
	networkPerformance = fields.NullableField(fields.StringField())
	normalizationSizeFactor = fields.NullableField(fields.Float32Field())
	operatingSystem = fields.NullableField(fields.StringField())
	operation = fields.NullableField(fields.StringField())
	physicalCores = fields.NullableField(fields.Int32Field())
	physicalProcessor = fields.NullableField(fields.StringField())
	preInstalledSw = fields.NullableField(fields.StringField())
	processorArchitecture = fields.NullableField(fields.StringField())
	processorFeatures = fields.NullableField(fields.StringField())
	productFamily = fields.NullableField(fields.StringField())
	provisioned = fields.NullableField(BooleanField())
	serviceCode = fields.NullableField(fields.StringField())
	serviceName = fields.NullableField(fields.StringField())
	storageIsEbsOnly = fields.NullableField(BooleanField())
	storageCount = fields.NullableField(fields.Int32Field())
	storageCapacity = fields.NullableField(fields.Int32Field())
	storageType = fields.NullableField(fields.StringField())
	storageMedia = fields.NullableField(fields.StringField())
	tenancy = fields.NullableField(fields.StringField())
	toLocation = fields.NullableField(fields.StringField())
	toLocationType = fields.NullableField(fields.StringField())
	transferType = fields.NullableField(fields.StringField())
	usageType = fields.NullableField(fields.StringField())
	vcpu = fields.NullableField(fields.Int32Field())
	volumeType = fields.NullableField(fields.StringField())
	
	onDemandAppliesTo = fields.NullableField(fields.StringField())
	onDemandBeginRange = fields.NullableField(fields.StringField())
	onDemandDescription = fields.NullableField(fields.StringField())
	onDemandEffectiveDate = fields.NullableField(fields.DateTimeField())
	onDemandEndRange = fields.NullableField(fields.Float32Field())
	onDemandOfferTermCode = fields.NullableField(fields.StringField())
	onDemandRateCode = fields.NullableField(fields.StringField())
	onDemandPricePerUnit = fields.NullableField(fields.StringField())
	onDemandPriceUnit = fields.NullableField(fields.StringField())

	reservedAppliesTo = fields.NullableField(fields.StringField())
	reservedBeginRange= fields.NullableField(fields.StringField())
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

	spotPrice = fields.NullableField(fields.StringField())
	spotTimestamp = fields.NullableField(fields.StringField())
	spotInstanceType = fields.NullableField(fields.StringField())
	spotAvailabilityZone = fields.NullableField(fields.StringField())

	engine = engines.Memory()

def capacityStatusNormalizer(key, value):
	if key == 'capacitystatus':
		return ('capacityStatus', value)
	else:
		pass

def clockSpeedNormalizer(key, value):
	if key == 'clockSpeed':
		clock_speed_is_up_to = False
		if re.findall("Up to", value):
			clock_speed_is_up_to = True
		clock_speed = float(re.findall("\d+\.\d+", value)[0])
		return ('clockSpeedIsUpTo', clock_speed_is_up_to), ('clockSpeed', clock_speed)
	else:
		pass

def dedicatedEbsThroughputNormalizer(key, value):
	if key == 'dedicatedEbsThroughput':
		dedicated_ebs_throughput_is_up_to = False
		if re.findall("Upto", value):
			dedicated_ebs_throughput_is_up_to = True
		dedicated_ebs_throughput = int(re.findall("\d+", value)[0])
		return ('dedicatedEbsThroughputIsUpTo', dedicated_ebs_throughput_is_up_to), ('dedicatedEbsThroughput', dedicated_ebs_throughput)
	else:
		pass

def ecuNormalizer(key, value):
	if key == 'ecu':
		if value == 'Variable':
			return ('ecuIsVariable', True)
		elif value == 'NA':
			return ('ecuIsVariable', False)
		else:
			return ('ecuIsVariable', False), ('ecu', float(value)) 

def instanceskuNormalizer(key, value):
	if key == 'instancesku':
		return ('instanceSKU', value)
	else:
		pass

def maxThroughputvolumeNormalizer(key, value):
	if key == 'maxThroughputvolume':
		return ('maxThroughputVolume', value)
	else:
		pass

def maxVolumeSizeNormalizer(key, value):
	if key == 'maxVolumeSize':
		max_volume_size = int(re.findall("\d+", value)[0])
		return ('maxVolumeSize', max_volume_size)
	else:
		pass

def memoryNormalizer(key, value):
	if key == 'memory':
		if value == 'NA':
			pass
		else:
			try:
				memory = float(re.findall("\d+\.\d+", value)[0])
			except(IndexError):
				try:
					memory = float(re.findall("\d+\,\d+", value)[0].replace(",", ""))
				except(IndexError):
					memory = float(re.findall("\d+", value)[0])
			return ('memory', memory)
	else:
		pass

def normalizationSizeFactorNormalizer(key, value):
	if key == 'normalizationSizeFactor':
		if value == 'NA':
			pass
		else:
			try:
				normalization_size_factor = float(re.findall("\d+\.\d+", value)[0])
			except(IndexError):
				normalization_size_factor = float(re.findall("\d+", value)[0])
			return ('normalizationSizeFactor', normalization_size_factor)
	else:
		pass

def servicecodeNormalizer(key, value):
	if key == 'servicecode':
		return('serviceCode', value)
	else:
		pass

def servicenameNormalizer(key, value):
	if key == 'servicename':
		return('serviceName', value)
	else:
		pass

def storageNormalizer(key, value):
	if key == 'storage':
		if value == 'EBS only':
			return ('storageIsEbsOnly', True)
		elif value != 'NA':
			storage_info = re.findall(r"(\d+)", value)
			storage_type = re.findall("\d+\s([^x]+)", value)[0]
			return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', storage_type)
		else:
			pass
	else:
		pass

def usagetypeNormalizer(key, value):
	if key == 'usagetype':
		return ('usageType', value)
	else:
		pass

def normalizeData(key, value):
	switcher = {
	'capacitystatus': capacityStatusNormalizer(key, value),
	'clockSpeed': clockSpeedNormalizer(key, value),
	'dedicatedEbsThroughput': dedicatedEbsThroughputNormalizer(key, value),
	'ecu': ecuNormalizer(key, value),
	'instancesku': instanceskuNormalizer(key, value),
	'maxThroughputvolume': maxThroughputvolumeNormalizer(key, value),
	'maxVolumeSize': maxVolumeSizeNormalizer(key, value),
	'memory': memoryNormalizer(key, value),
	'normalizationSizeFactor': normalizationSizeFactorNormalizer(key, value),
	'servicecode': servicecodeNormalizer(key, value),
	'servicename': servicenameNormalizer(key, value),
	'storage': storageNormalizer(key, value),
	'usagetype': usagetypeNormalizer(key, value)
	}
	func = switcher.get(key, lambda: (key, str(value)))

	try:
		if func() == None:
			pass
		else:
			return func()
	except(TypeError):
		if func == None:
			pass
		else:
			return func

def getData(d, mylist):
	data = {}
	for sku, details in d.items():
		values = []
		a = d.get(sku)
		for i in mylist:
			try:
				try:
					if normalizeData(i, a[i]) == None:
						pass
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
		try:
			data[sku].append(values)
		except KeyError:
			data[sku] = values
	return data

from copy import deepcopy

def dict_of_dicts_merge(x, y):
    z = {}
    overlapping_keys = x.keys() & y.keys()
    for key in overlapping_keys:
        z[key] = dict_of_dicts_merge(x[key], y[key])
    for key in x.keys() - overlapping_keys:
        z[key] = deepcopy(x[key])
    for key in y.keys() - overlapping_keys:
        z[key] = deepcopy(y[key])
    return z

def load():
	'''
	Loads data from local JSON files into database
	TODO: Load data from s3 buckets
	'''
	db = Database('contrail')
	db.create_table(InstanceData)
	fil = open('tmp.json')
	fil2 = open('spot_data.json')
	d = json.load(fil)
	d2 = json.load(fil2)

	product_dict, on_demand_dict, reserved_dict, product_keys, on_demand_keys, reserved_keys = getAllAttributes(d)
	spot_data = getSpotData(d2, product_keys + on_demand_keys + reserved_keys)
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
	
	items = list(data.values()) + spot_data
	for item in items:
		instance = InstanceData()
		for i in item:
			setattr(instance, i[0], i[1])
		db.insert([instance])

if __name__ == '__main__':
	load()