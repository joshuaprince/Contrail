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
        try:
            clock_speed = float(re.findall("\d+\.\d+", value)[0])
        except(IndexError):
            clock_speed = float(re.findall("\d+", value)[0])
        return ('clockSpeedIsUpTo', clock_speed_is_up_to), ('clockSpeed', clock_speed)
    else:
        pass

def dedicatedEbsThroughputNormalizer(key, value):
    if key == 'dedicatedEbsThroughput' and value != 'N/A':
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
            try:
                storage_info = re.findall(r"(\d+)", value)
                storage_type = re.findall("\d+\s([^x]+)", value)[0]
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', storage_type)
            except(IndexError):
                storage_info = re.findall(r"(\d+)", value)
                return ('storageIsEbsOnly', False), ('storageCount', storage_info[0]), ('storageCapacity', storage_info[1]), ('storageType', "HDD")
        else:
            pass
    else:
        pass

def usagetypeNormalizer(key, value):
    if key == 'usagetype':
        return ('usageType', value)
    else:
        pass

def USDNormalizer(key, value):
    if key == 'uSD':
        return ('pricePerHour', value)
    else:
        pass

def unitNormalizer(key, value):
    if key == 'unit':
        return ('priceUnit', value)
    else:
        pass

def spotPriceNormalizer(key, value):
    if key == 'spotPrice':
        return ('pricePerHour', value)
    else:
        pass

def servicecodeNormalizer(key, value):
    if key == 'servicecode':
        return ('provider', value)
    else:
        pass 

def regionNormalizer(key, value):
    if key == 'region':
        regions = {
        'usgoveast1': 'AWS Gov US East',
        'usgovewest1': 'AWS Gov US West',
        'apnortheast1': 'Asia Pacific Northeast 1',
        'apnortheast2': 'Asia Pacific Northeast 2',
        'apnortheast3': 'Asia Pacific Northeast 3',
        'apsoutheast1': 'Asia Pacific Southeast 1',
        'apsoutheast2': 'Asia Pacific Southeast 2',
        'asiaeast1': 'Asia East 1',
        'asiaeast2': 'Asia East 2',
        'asianortheast1': 'Asia Northeast 1', 
        'asianortheast2': 'Asia Northeast 2',
        'asiasouth1': 'Asia South 1',
        'asiasoutheast1': 'Asia Southeast 1',
        'australiasoutheast1': 'Australia Southeast 1',
        'cacentral1': 'Canada 1',
        'cnnorth1': 'China North 1',
        'cnnorthwest1': 'China Northwest 1',
        'eucentral1': 'Europe Central 1',
        'euwest1': 'Europe West 1',
        'euwest2': 'Europe West 2',
        'euwest3': 'Europe West 3',
        'eunorth1': 'Europe North 1',
        'europenorth1': 'Europe North 1',
        'europewest1': 'Europe West 1',
        'europewest2': 'Europe West 2',
        'europewest3': 'Europe West 3',
        'europewest4': 'Europe West 4',
        'europewest6': 'Europe West 6',
        'northamericanortheast1': 'North America Northeast 1',
        'saeast1': 'South America East 1',
        'southamericaeast1': 'South America East 1',
        'uscentral1': 'US Central 1',
        'useast1': 'US East 1',
        'useast2': 'US East 2',
        'useast4': 'US East 4',
        'uswest1': 'US West 1',
        'uswest2': 'US West 2'
        }
        return ('region', regions[value])
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
    'uSD': USDNormalizer(key, value),
    'unit': unitNormalizer(key, value),
    'spotPrice': spotPriceNormalizer(key, value),
    'region': regionNormalizer(key, value),
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