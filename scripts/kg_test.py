import argparse
import os, sys

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentDir)
import config
import models

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--weighted', type=bool, required=False)
parser.add_argument('--version', type=str, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method
order = parsedConfig.order
weighted = parsedConfig.weighted if parsedConfig.weighted else False
version = parsedConfig.version if parsedConfig.version else ('weighted' if weighted else 'retested')

logDir = parentDir + '/log/%s/' % database
logPath = logDir + '%s.log' % method
f = open(logPath, 'r')
s = f.read().split('\n')
f.close()

last = 0
rawResults = []
for i in range(len(s)):
    if '-' * 50 in s[i]:
        rawResults.append(s[last:i])
        last = i + 1

newLogPath = logDir + '%s%s.log' % (method, '' if version == 'overwrite' else '_' + version)
if order == 1:
    f = open(newLogPath, 'w')
    f.close()

dimension = dict()
model = dict()
startLines = dict()
endLines = dict()
for rawResult in rawResults:
    seqNum = int(rawResult[0].split('_')[1])
    model[seqNum] = rawResult[0].split('_')[0][1:]
    for i in range(1, len(rawResult)):
        if '--dimension:' in rawResult[i]:
            dimension[seqNum] = int(rawResult[i].split('\t')[1])
        if not '--' in rawResult[i]:
            break
    startLines[seqNum] = rawResult[:i]
    endLines[seqNum] = rawResult[-2:]

resultDir = parentDir + '/res/%s/%s/' % (database, method)
benchmarkDir = parentDir + '/benchmarks/%s/' % database
fileList = os.listdir(resultDir)

importPath = resultDir + '%s/model.vec.tf' % order

f = open(newLogPath, 'a')
f.write('\n'.join(startLines[order]) + '\n\n')
f.close()

params = config.Config()
params.set_in_path(benchmarkDir)
params.set_test_flag(True)
params.set_work_threads(32)
params.set_dimension(dimension[order])
params.set_import_files(importPath)
params.set_test_link_prediction(True)
params.set_test_weighted(weighted)
params.init()
exec('params.set_model(models.%s)' % model[order])
params.test(newLogPath)

f = open(newLogPath, 'a')
f.write('\n' + '\n'.join(endLines[order]) + '\n')
f.write('-' * 50 + '\n')
f.close()
