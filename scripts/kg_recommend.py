import argparse
import os, sys

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentDir)
import config
import models


def getBestOrder(database, method):
    try:
        analyzedLogPath = parentDir + '/log/%s/analyzed/%s_analyzed.log' % (database, method)
        f = open(analyzedLogPath, 'r')
        s = f.read().split('\n')
        f.close()

        bestOrder = int(s[1].split()[1])
        return bestOrder
    except:
        return 1


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def getDimension(method, order):
    configPath = parentDir + '/scripts/config/%s.config' % method
    f = open(configPath, 'r')
    s = f.read().split('\n')
    f.close()

    configLine = s[order]
    return int(configLine.split('dimension=')[1].split()[0])


def generateRecommendFile(relation, recommendObject):
    f = open(benchmarkDir + 'type_constrain.txt', 'r')
    s = f.read().split('\n')
    f.close()

    f = open(benchmarkDir + 'recommend2id.txt', 'w')
    line = s[relation * 2 + 2 - recommendObject].strip()
    splited = line.split()
    f.write(splited[1] + '\n')
    for i in range(2, len(splited)):
        f.write('%s %s %s\n' % (1 - recommendObject, relation, splited[i]))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--relation', type=int, required=True)
parser.add_argument('--object', type=int, required=True)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method
order = parsedConfig.order if parsedConfig.order else getBestOrder(database, method)
relation = parsedConfig.relation
recommendObject = parsedConfig.object  # 0: recommend head, 1: recommend tail;

model = method.split('_')[0]

mkdir(['res', database, method, order, 'recommendation'])
recommendLogPath = parentDir + '/res/%s/%s/%s/recommendation/recommendation_relation=%s_recommend=%s.log' \
                   % (database, method, order, relation, 'tail' if recommendObject else 'head')
f = open(recommendLogPath, 'w')
f.close()

resultDir = parentDir + '/res/%s/%s/' % (database, method)
benchmarkDir = parentDir + '/benchmarks/%s/' % database

generateRecommendFile(relation, recommendObject)

importPath = resultDir + '%s/model.vec.tf' % order

params = config.Config()
params.set_in_path(benchmarkDir)
params.set_test_flag(True)
params.set_work_threads(32)
params.set_dimension(getDimension(method, order))
params.set_import_files(importPath)
params.set_test_recommendation(True)
params.set_recommend_result_path(recommendLogPath)
params.init()
exec('params.set_model(models.%s)' % model)
params.test()
