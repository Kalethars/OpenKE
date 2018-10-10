import tensorflow as tf
import numpy as np
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

    log.write('Total Time: ' + str(time.time() - startTime) + ' seconds\n')
    log.write('End of ' + module + '\n')
    log.write('-' * 50 + '\n')
    module = '/'.join(module.split('/')[:-1])

    log.close()


def initVariables(co_name):
    global logPath, module, startTime, parentdir

    module = ''
    startTime = time.time()
    logPath = parentDir + '/log/' + co_name + '.log'
    log = open(logPath, 'w')
    log.close()


def initParams(map):
    params = config.Config()

    params.set_test_flag(True)
    params.set_ent_neg_rate(1)
    params.set_rel_neg_rate(0)

    params.set_test_triple_classification(False)
    params.set_test_link_prediction(True)

    params.set_train_times(int(map['epoch']))
    params.set_nbatches(int(map['nbatches']))
    params.set_alpha(float(map['alpha']))
    params.set_margin(float(map['margin']))
    params.set_bern(int(map['bern']))
    params.set_dimension(int(map['dimension']))

    return params


def parseParams(line):
    paramMap = dict()
    splitedLine = line.split()
    for each in splitedLine:
        pos = each.find('=')
        if pos >= 0:
            paramMap[each[:pos]] = each[pos + 1:]
    return paramMap


def TransE():
    global logPath, threads, start, count, dataset

    name = 'TransE'
    initVariables(name)

    begin(name)

    for i in range(start, start + count):
        begin(name + '_' + str(i))

        paramMap = parseParams(configLines[i])

        params = initParams(paramMap)
        params.set_in_path(dataset)
        params.set_work_threads(threads)
        params.set_opt_method("SGD")

        exportPath = parentDir + '/res/' + name + '/' + str(i) + '/model.vec.tf'
        outPath = parentDir + '/res/' + name + '/' + str(i) + '/embedding.vec.json'

        params.set_export_files(exportPath)
        params.set_out_files(outPath)

        params.init()
        params.set_model(models.TransE)
        params.run()
        params.test(logPath)

        f = open(logPath, 'a')
        f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
        f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
        f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
        f.write('--margin:\t%f\n' % float(paramMap['margin']))
        f.write('--bern:\t%d\n' % int(paramMap['bern']))
        f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
        f.close()

        end()

    end()


def TransH():
    global logPath, threads, start, count, dataset

    name = 'TransH'
    initVariables(name)

    begin(name)

    for i in range(start, start + count):
        begin(name + '_' + str(i))

        paramMap = parseParams(configLines[i])

        params = initParams(paramMap)
        params.set_in_path(dataset)
        params.set_work_threads(threads)
        params.set_opt_method("SGD")

        exportPath = parentDir + '/res/' + name + '/' + str(i) + '/model.vec.tf'
        outPath = parentDir + '/res/' + name + '/' + str(i) + '/embedding.vec.json'

        params.set_export_files(exportPath)
        params.set_out_files(outPath)

        params.init()
        params.set_model(models.TransE)
        params.run()
        params.test(logPath)

        f = open(logPath, 'a')
        f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
        f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
        f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
        f.write('--margin:\t%f\n' % float(paramMap['margin']))
        f.write('--bern:\t%d\n' % int(paramMap['bern']))
        f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
        f.close()

        end()

    end()


def DistMult():
    global logPath, threads, start, count, dataset

    name = 'DistMult'
    initVariables(name)

    begin(name)

    for i in range(start, start + count):
        begin(name + '_' + str(i))

        paramMap = parseParams(configLines[i])

        params = initParams(paramMap)
        params.set_in_path(dataset)
        params.set_work_threads(threads)
        params.set_opt_method("Adagrad")

        exportPath = parentDir + '/res/' + name + '/' + str(i) + '/model.vec.tf'
        outPath = parentDir + '/res/' + name + '/' + str(i) + '/embedding.vec.json'

        params.set_export_files(exportPath)
        params.set_out_files(outPath)

        params.init()
        params.set_model(models.DistMult)
        params.run()
        params.test(logPath)

        f = open(logPath, 'a')
        f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
        f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
        f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
        f.write('--margin:\t%f\n' % float(paramMap['margin']))
        f.write('--bern:\t%d\n' % int(paramMap['bern']))
        f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
        f.close()

        end()

    end()


def ComplEx():
    global logPath, threads, start, count, dataset

    name = 'ComplEx'
    initVariables(name)

    begin(name)

    for i in range(start, start + count):
        begin(name + '_' + str(i))

        paramMap = parseParams(configLines[i])

        params = initParams(paramMap)
        params.set_in_path(dataset)
        params.set_work_threads(threads)
        params.set_lmbda(float(paramMap['lmbda']))
        params.set_opt_method("Adagrad")

        exportPath = parentDir + '/res/' + name + '/' + str(i) + '/model.vec.tf'
        outPath = parentDir + '/res/' + name + '/' + str(i) + '/embedding.vec.json'

        params.set_export_files(exportPath)
        params.set_out_files(outPath)

        params.init()
        params.set_model(models.DistMult)
        params.run()
        params.test(logPath)

        f = open(logPath, 'a')
        f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
        f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
        f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
        f.write('--margin:\t%f\n' % float(paramMap['margin']))
        f.write('--bern:\t%d\n' % int(paramMap['bern']))
        f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
        f.close()

        end()

    end()


parser = argparse.ArgumentParser()
parser.add_argument('--config', type=str, required=True)
parser.add_argument('--method', type=str, required=True)
parsedConfig = parser.parse_args()

f = open(parsedConfig.config, 'r')
configLines = f.readlines()
f.close()

map = parseParams(configLines[0])
threads = int(map['threads'])
start = int(map['start'])
count = int(map['count'])
dataset = parentDir + '/benchmark/' + map['dataset']

method = parsedConfig.method.lower()
if method == 'transe':
    TransE()
elif method == 'transh':
    TransH()
elif method == 'distmult':
    DistMult()
elif method == 'complex':
    ComplEx()
else:
    print
    'Invalid method!'
