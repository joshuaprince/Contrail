import re


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

def onDemandUnit(key, value):
    if key == 'onDemandUnit':
        return ('onDemandPriceUnit', value)
    else:
        pass

def onDemandUSD(key, value):
    if key == 'onDemandUSD':
        return ('onDemandPricePerUnit', value)
    else:
        pass

def reservedUnit(key, value):
    if key == 'reservedUnit':
        return ('reservedPriceUnit', value)
    else:
        pass

def reservedUSD(key, value):
    if key == 'reservedUSD':
        return ('reservedPricePerUnit', value)
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
    'usagetype': usagetypeNormalizer(key, value),
    'onDemandUnit': onDemandUnit(key, value),
    'onDemandUSD': onDemandUSD(key, value),
    'reservedUnit': reservedUnit(key, value),
    'reservedUSD': reservedUSD(key, value)
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
