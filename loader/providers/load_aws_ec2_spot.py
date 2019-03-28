import collections
import itertools
import re

def capacityStatus(key, value):
    if key == 'capacitystatus':
        return ('capacityStatus', value)
    else:
        pass

def clockSpeed(key, value):
    if key == 'clockSpeed':
        clockSpeedIsUpTo = False
        if re.findall("Up to", value):
            clockSpeedIsUpTo = True
        clockSpeed = float(re.findall("\d+\.\d+", value)[0])
        return ('clockSpeedIsUpTo', clockSpeedIsUpTo), ('clockSpeed', clockSpeed)
    else:
        pass

def dedicatedEbsThroughput(key, value):
    if key == 'dedicatedEbsThroughput':
        dedicatedEbsThroughputIsUpTo = False
        if re.findall("Upto", value):
            dedicatedEbsThroughputIsUpTo = True
        dedicatedEbsThroughput = int(re.findall("\d+", value)[0])
        return ('dedicatedEbsThroughputIsUpTo', dedicatedEbsThroughputIsUpTo), ('dedicatedEbsThroughput', dedicatedEbsThroughput)
    else:
        pass

def ecu(key, value):
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
            try:
                storage_type = re.findall("\d+\s([^x]+)", value)[0]
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', storage_type)
            except(IndexError):
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', 'HDD')
        else:
            pass
    else:
        pass

def usagetypeNormalizer(key, value):
    if key == 'usagetype':
        return ('usageType', value)
    else:
        pass

def spotPrice(key, value):
    if key == 'SpotPrice':
        return ('spotPrice', value)
    else:
        pass

def timestamp(key, value):
    if key == 'Timestamp':
        return ('spotTimestamp', value)
    else: 
        pass

def instanceType(key, value):
    if key == 'InstanceType':
        return ('spotInstanceType', value)
    else:
        pass

def availabilityZone(key, value):
    if key == 'AvailabilityZone':
        return ('spotAvailabilityZone', value)
    else:
        pass


def normalizeData(key, value):
    switcher = {
    'capacitystatus': capacityStatus(key, value),
    'clockSpeed': clockSpeed(key, value),
    'dedicatedEbsThroughput': dedicatedEbsThroughput(key, value),
    'ecu': ecu(key, value),
    'instancesku': instanceskuNormalizer(key, value),
    'maxThroughputvolume': maxThroughputvolumeNormalizer(key, value),
    'maxVolumeSize': maxVolumeSizeNormalizer(key, value),
    'memory': memoryNormalizer(key, value),
    'normalizationSizeFactor': normalizationSizeFactorNormalizer(key, value),
    'servicecode': servicecodeNormalizer(key, value),
    'servicename': servicenameNormalizer(key, value),
    'storage': storageNormalizer(key, value),
    'usagetype': usagetypeNormalizer(key, value),
    'SpotPrice': spotPrice(key, value),
    'Timestamp': timestamp(key, value),
    'InstanceType': instanceType(key, value),
    'AvailabilityZone': availabilityZone(key, value)
    }
    func = switcher.get(key, lambda: (key, value))

    try:
        return func()
    except(TypeError):
        return func

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
                try:
                    if normalizeData(i, instance[i]) == None:
                        pass
                    else:
                        key, value = normalizeData(i, instance[i])
                except(ValueError):
                    values.extend(normalizeData(i, instance[i]))
                    pass
                if isinstance(value, tuple):
                    values.extend((key, value))
                else:
                    values.append((key, value))
            except(KeyError, AttributeError):
                pass
        data.append(values)
    return data
