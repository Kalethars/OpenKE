import config
import models
import tensorflow as tf
import numpy as np
import argparse
import time


class KgTrain(object):
    def begin(self, co_name):
        log = open(self.logPath, 'a')

        self.module += '/' + co_name
        self.startTime = time.time()
        log.write(self.module + '\n')

        log.close()

    def end(self):
        log = open(self.logPath, 'a')

        log.write('Total Time: ' + str(time.time() - self.startTime) + ' seconds\n')
        log.write('End of ' + self.module + '\n')
        log.write('-' * 50 + '\n')
        self.module = '/'.join(self.module.split('/')[:-1])

        log.close()

    def initVariables(self, co_name):
        self.module = ''
        self.startTime = time.time()
        self.logPath = '../log/' + co_name + '.log'
        log = open(self.logPath, 'w')
        log.close()

    def initParams(self, map):
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

    def parseParams(self, line):
        paramMap = dict()
        splitedLine = line.split()
        for each in splitedLine:
            pos = each.find('=')
            if pos >= 0:
                paramMap[each[:pos]] = each[pos + 1:]
        return paramMap

    def TransE(self):
        name = 'TransE'
        self.initVariables(name)

        self.begin(name)

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True)
        parsedConfig = parser.parse_args()

        f = open(parsedConfig.config, 'r')
        configLines = f.readlines()
        f.close()

        paramMap = self.parseParams(configLines[0])
        threads = int(paramMap['threads'])
        start = int(paramMap['start'])
        count = int(paramMap['count'])

        for i in range(start, start + count):
            self.begin(name + '_' + str(i))

            paramMap = self.parseParams(configLines[i])

            params = self.initParams(paramMap)
            params.set_work_threads(threads)
            params.set_opt_method("SGD")

            exportPath = '../res/' + name + '/' + str(i) + '/model.vec.tf'
            outPath = '../res/' + name + '/' + str(i) + '/embedding.vec.json'

            params.set_export_files(exportPath)
            params.set_out_files(outPath)

            params.init()
            params.set_model(models.TransE)
            params.run()
            params.test(self.logPath)

            f = open(self.logPath, 'a')
            f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
            f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
            f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
            f.write('--margin:\t%f\n' % float(paramMap['margin']))
            f.write('--bern:\t%d\n' % int(paramMap['bern']))
            f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
            f.close()

            self.end()

        self.end()

    def TransH(self):
        name = 'TransH'
        self.initVariables(name)

        self.begin(name)

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True)
        parsedConfig = parser.parse_args()

        f = open(parsedConfig.config, 'r')
        configLines = f.readlines()
        f.close()

        paramMap = self.parseParams(configLines[0])
        threads = int(paramMap['threads'])
        start = int(paramMap['start'])
        count = int(paramMap['count'])

        for i in range(start, start + count):
            self.begin(name + '_' + str(i))

            paramMap = self.parseParams(configLines[i])

            params = self.initParams(paramMap)
            params.set_work_threads(threads)
            params.set_opt_method("SGD")

            exportPath = '../res/' + name + '/' + str(i) + '/model.vec.tf'
            outPath = '../res/' + name + '/' + str(i) + '/embedding.vec.json'

            params.set_export_files(exportPath)
            params.set_out_files(outPath)

            params.init()
            params.set_model(models.TransE)
            params.run()
            params.test(self.logPath)

            f = open(self.logPath, 'a')
            f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
            f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
            f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
            f.write('--margin:\t%f\n' % float(paramMap['margin']))
            f.write('--bern:\t%d\n' % int(paramMap['bern']))
            f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
            f.close()

            self.end()

        self.end()

    def DistMult(self):
        name = 'DistMult'
        self.initVariables(name)

        self.begin(name)

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True)
        parsedConfig = parser.parse_args()

        f = open(parsedConfig.config, 'r')
        configLines = f.readlines()
        f.close()

        paramMap = self.parseParams(configLines[0])
        threads = int(paramMap['threads'])
        start = int(paramMap['start'])
        count = int(paramMap['count'])

        for i in range(start, start + count):
            self.begin(name + '_' + str(i))

            paramMap = self.parseParams(configLines[i])

            params = self.initParams(paramMap)
            params.set_work_threads(threads)
            params.set_opt_method("Adagrad")

            exportPath = '../res/' + name + '/' + str(i) + '/model.vec.tf'
            outPath = '../res/' + name + '/' + str(i) + '/embedding.vec.json'

            params.set_export_files(exportPath)
            params.set_out_files(outPath)

            params.init()
            params.set_model(models.DistMult)
            params.run()
            params.test(self.logPath)

            f = open(self.logPath, 'a')
            f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
            f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
            f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
            f.write('--margin:\t%f\n' % float(paramMap['margin']))
            f.write('--bern:\t%d\n' % int(paramMap['bern']))
            f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
            f.close()

            self.end()

        self.end()

    def ComplEx(self):
        name = 'ComplEx'
        self.initVariables(name)

        self.begin(name)

        parser = argparse.ArgumentParser()
        parser.add_argument('--config', type=str, required=True)
        parsedConfig = parser.parse_args()

        f = open(parsedConfig.config, 'r')
        configLines = f.readlines()
        f.close()

        paramMap = self.parseParams(configLines[0])
        threads = int(paramMap['threads'])
        start = int(paramMap['start'])
        count = int(paramMap['count'])

        for i in range(start, start + count):
            self.begin(name + '_' + str(i))

            paramMap = self.parseParams(configLines[i])

            params = self.initParams(paramMap)
            params.set_work_threads(threads)
            params.set_lmbda(float(paramMap['lmbda']))
            params.set_opt_method("Adagrad")

            exportPath = '../res/' + name + '/' + str(i) + '/model.vec.tf'
            outPath = '../res/' + name + '/' + str(i) + '/embedding.vec.json'

            params.set_export_files(exportPath)
            params.set_out_files(outPath)

            params.init()
            params.set_model(models.DistMult)
            params.run()
            params.test(self.logPath)

            f = open(self.logPath, 'a')
            f.write('--epoch:\t%d\n' % int(paramMap['epoch']))
            f.write('--nbatches:\t%d\n' % int(paramMap['nbatches']))
            f.write('--alpha:\t%f\n' % float(paramMap['alpha']))
            f.write('--margin:\t%f\n' % float(paramMap['margin']))
            f.write('--bern:\t%d\n' % int(paramMap['bern']))
            f.write('--dimension:\t%d\n' % int(paramMap['dimension']))
            f.close()

            self.end()

        self.end()
