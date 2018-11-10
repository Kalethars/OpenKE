import argparse
import os, sys

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentDir)
import config
import models

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method

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

newLogPath = logDir + '%s_retested.log' % method
f=open(newLogPath,'w')
f.close()

dimension = dict()
model = dict()
startLines = dict()
endLines = dict()
for rawResult in rawResults:
    seqNum = rawResult[0].split('_')[1]
    model[seqNum] = rawResult[0].split('_')[0][1:]
    for i in range(1, len(rawResult)):
        if '--dimension=' in rawResult[i]:
            dimension = int(rawResult[i].split('=')[1])
        if not '--' in rawResult[i]:
            break
    startLines[seqNum] = rawResult[:i]
    endLines[seqNum] = rawResult[-2:]

resultDir = parentDir + '/res/%s/%s/' % (database, method)
benchmarkDir = parentDir + '/benchmarks/%s/' % database
fileList = os.listdir(resultDir)
for seqNum in sorted(fileList, key=lambda x: int(x)):
    importPath = resultDir + '%s/model.vec.tf' % seqNum

    f = open(newLogPath,'a')
    f.write('\n'.join(startLines[i]))
    params = config.Config()
    params.set_in_path(benchmarkDir)
    params.set_test_flag(True)
    params.set_work_threads(32)
    params.set_dimension(dimension[seqNum])
    params.set_import_files(importPath)
    params.init()
    exec('params.set_model(models.%s)' % model[seqNum])
    params.test(newLogPath)
