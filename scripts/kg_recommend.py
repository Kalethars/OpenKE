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


def generateTypeConstraint():
    f = open(benchmarkDir + 'triplets.txt', 'r')
    s = f.read().split('\n')
    f.close()

    legalEntities = set()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        legalEntities.add(splited[0])
        legalEntities.add(splited[2])

    f = open(benchmarkDir + 'entity2id.txt', 'r')
    s = f.read().split('\n')
    f.close()

    entityIndex = dict()
    typeCount = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 2:
            continue
        if not splited[0] in legalEntities:
            continue
        entityIndex[splited[0]] = splited[1]
        typeCount[splited[0][0]] = typeCount.get(splited[0][0], 0) + 1

    relationMap = {'0': ('a', 'i'),
                   '1': ('a', 'f'),
                   '2': ('p', 'a'),
                   '3': ('p', 'f'),
                   '4': ('p', 'v'),
                   '5': ('p', 'p'),
                   '6': ('f', 'f')
                   }
    relationCount = len(relationMap)
    headCount = sum([typeCount[relationMap[relation][0]] for relation in relationMap.keys()])
    tailCount = sum([typeCount[relationMap[relation][1]] for relation in relationMap.keys()])

    os.rename(benchmarkDir + 'type_constrain.txt', benchmarkDir + 'type_constrain.bak')
    f = open(benchmarkDir + 'type_constrain.txt', 'w')
    f.write('%i\t%i\t%i\n' % (relationCount, headCount, tailCount))
    for relation in sorted(relationMap.keys()):
        for object in range(2):
            typ = relationMap[relation][object]
            f.write('%s\t%i' % (relation, typeCount[typ]))
            for entity in entityIndex.keys():
                if entity[0] == typ:
                    f.write('\t%s' % entityIndex[entity])
            f.write('\n')
    f.close()


def revertTypeConstraint():
    os.remove(benchmarkDir + 'type_constrain.txt')
    os.rename(benchmarkDir + 'type_constrain.bak', benchmarkDir + 'type_constrain.txt')


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--relation', type=int, required=True)
parser.add_argument('--object', type=int, required=True)
parser.add_argument('--replace', type=int, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method
order = parsedConfig.order if parsedConfig.order else getBestOrder(database, method)
relation = parsedConfig.relation
recommendObject = parsedConfig.object  # 0: recommend head, 1: recommend tail;
replaceTypeConstraint = parsedConfig.replace if parsedConfig.replace is not None else 1

model = method.split('_')[0]

mkdir(['res', database, method, order, 'recommendation', 'raw'])
recommendLogPath = parentDir + '/res/%s/%s/%s/recommendation/raw/recommendation_relation=%s_recommend=%s.log' \
                   % (database, method, order, relation, 'tail' if recommendObject else 'head')
f = open(recommendLogPath, 'w')
f.close()

resultDir = parentDir + '/res/%s/%s/' % (database, method)
benchmarkDir = parentDir + '/benchmarks/%s/' % database

if replaceTypeConstraint:
    generateTypeConstraint()
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

if replaceTypeConstraint:
    revertTypeConstraint()
