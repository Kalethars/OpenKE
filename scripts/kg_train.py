import argparse
import time
import os, sys

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentDir)
import config
import models


def begin(co_name):
    global logPath, module, startTime

    log = open(logPath, 'a')

    module += '/' + co_name
    startTime = time.time()
    log.write(module + '\n')

    log.close()


def end():
    global logPath, module, startTime

    log = open(logPath, 'a')

    log.write('\n')
    log.write('Total Time: ' + str(time.time() - startTime) + ' seconds\n')
    log.write('End of ' + module + '\n')
    log.write('-' * 50 + '\n')
    module = '/'.join(module.split('/')[:-1])

    log.close()


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def initVariables():
    global logPath, module, startTime, order

    module = ''
    startTime = time.time()
    logPath = parentDir + '/log/%s/%s.log' % (database, configName)
    if order == '1':
        log = open(logPath, 'w')
    else:
        log = open(logPath, 'a')
    log.close()


def initParams(map):
    params = config.Config()

    params.set_test_flag(True)
    params.set_ent_neg_rate(1)
    params.set_rel_neg_rate(0)

    params.set_test_triple_classification(False)
    params.set_test_link_prediction(True)
    params.set_train_weighted(bool(map['weighted']))

    params.set_train_times(int(map['epoch']))
    params.set_nbatches(int(map['nbatches']))
    params.set_alpha(float(map['alpha']))
    params.set_margin(float(map['margin']))
    params.set_bern(int(map['bern']))
    params.set_dimension(int(map['dimension']))

    return params


def parseParams(line, output=True):
    def verify(map, key, cls):
        try:
            tmp = cls(map[key])
        except:
            raise ValueError('Invalid param %s!' % key)

    global logPath

    paramMap = dict()
    splitedLine = line.split()
    for each in splitedLine:
        pos = each.find('=')
        if pos >= 0:
            paramMap[each[:pos]] = each[pos + 1:]

    if output:
        verify(paramMap, 'epoch', int)
        verify(paramMap, 'nbatches', int)
        verify(paramMap, 'alpha', float)
        verify(paramMap, 'margin', float)
        verify(paramMap, 'bern', int)
        verify(paramMap, 'dimension', int)
        verify(paramMap, 'weighted', bool)

        f = open(logPath, 'a')
        f.write('--epoch:\t%s\n' % paramMap['epoch'])
        f.write('--nbatches:\t%s\n' % paramMap['nbatches'])
        f.write('--alpha:\t%s\n' % paramMap['alpha'])
        f.write('--margin:\t%s\n' % paramMap['margin'])
        f.write('--bern:\t%s\n' % paramMap['bern'])
        f.write('--dimension:\t%s\n' % paramMap['dimension'])
        f.write('--weighted:\t%s\n' % paramMap['weighted'])
        f.write('\n')
        f.close()

    return paramMap


def TransE():
    global logPath, order, configLine

    name = 'TransE'
    initVariables()

    begin(name + '_' + str(order))

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("SGD")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.TransE)
    params.run()
    params.test(logPath)

    end()


def TransH():
    global logPath, order, configLine

    name = 'TransH'
    initVariables()

    begin(name + '_' + order)

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("SGD")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.TransH)
    params.run()
    params.test(logPath)

    end()


def DistMult():
    global logPath, order, configLine

    name = 'DistMult'
    initVariables()

    begin(name + '_' + order)

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("Adagrad")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.DistMult)
    params.run()
    params.test(logPath)

    end()


def ComplEx():
    global logPath, order, configLine

    name = 'ComplEx'
    initVariables()

    begin(name + '_' + order)

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_lmbda(float(paramMap['lmbda']))
    params.set_opt_method("Adagrad")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.ComplEx)
    params.run()
    params.test(logPath)

    end()


def HolE():
    global logPath, order, configLine

    name = 'HolE'
    initVariables()

    begin(name + '_' + order)

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("Adagrad")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.HolE)
    params.run()
    params.test(logPath)

    end()


def WTransE(norm2=False):
    global logPath, order, configLine

    name = 'WTransE' + '2' if norm2 else ''
    initVariables()

    begin(name + '_' + str(order))

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("SGD")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    if not norm2:
        params.set_model(models.WTransE)
    else:
        params.set_model(models.WTransE2)
    params.run()
    params.test(logPath)

    end()


def WTransH():
    global logPath, order, configLine

    name = 'WTransH'
    initVariables()

    begin(name + '_' + order)

    paramMap = parseParams(configLine)

    params = initParams(paramMap)
    params.set_in_path(databasePath)
    params.set_work_threads(threads)
    params.set_opt_method("SGD")

    mkdir(['res', database, configName, order])
    exportPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/model.vec.tf'
    outPath = parentDir + '/res/' + database + '/' + configName + '/' + order + '/embedding.vec.json'

    params.set_export_files(exportPath)
    params.set_out_files(outPath)

    params.init()
    params.set_model(models.WTransH)
    params.run()
    params.test(logPath)

    end()


mkdir(['log'])
mkdir(['res'])
parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, required=True)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parsedConfig = parser.parse_args()

f = open(parsedConfig.config, 'r')
configLines = f.readlines()
f.close()
configName = parsedConfig.config.split('/')[-1].split('.')[0]

map = parseParams(configLines[0], False)
threads = int(map['threads'])
database = map['database']
databasePath = parentDir + '/benchmarks/' + map['database'] + '/'

order = str(parsedConfig.order)
configLine = configLines[parsedConfig.order]

method = parsedConfig.method.lower()
if method == 'transe':
    TransE()
elif method == 'transh':
    TransH()
elif method == 'distmult':
    DistMult()
elif method == 'complex':
    ComplEx()
elif method == 'hole':
    HolE()
elif method == 'wtranse':
    WTransE()
elif method == 'wtranse2':
    WTransE(True)
elif method == 'wtransh':
    WTransH()
else:
    raise ValueError('Invalid method!')
