from __future__ import print_function
from __future__ import division

import numpy as np

import argparse
import os
import codecs
import time
import gc

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

times = 0
timesTotal = 0
startTime = 0


def output(f, s='', end='\n'):
    print(s + end, end='')
    if not f is None:
        f.write(s + end)


def startTiming(total):
    global times, timesTotal, startTime

    times = 0
    startTime = time.time()
    timesTotal = int(total)

    print('Total loops: %i' % timesTotal)


def displayTiming():
    global times, timesTotal, startTime

    times += 1
    print('\r%s\t%.2fs' % (str(round(100. * times / timesTotal, 2)) + '%', time.time() - startTime), end='')
    if times == timesTotal:
        print()


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


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def loadEntityInfo(typ):
    f = codecs.open(parentDir + '/data/%s/info/%sInfo.data' % (database, typ), 'r', encoding='utf-8', errors='ignore')
    infoLines = f.read().split('\n')
    f.close()

    sortedEntityInfo = []
    for i in range(len(infoLines)):
        splited = infoLines[i].split('\t')
        if typ != 'venue':
            if len(splited) != 2:
                continue
        else:
            if len(splited) != 5:
                continue
        entityId = splited[0]
        sortedEntityInfo.append(entityId)

    return sortedEntityInfo


def loadRelationEntityDistances(relations, directions):
    print('Loading distances...')

    distmapDir = parentDir + '/res/%s/%s/%i/distmap/' % (database, method, order)
    relationEntityDistances = []
    for i in range(len(relations)):
        relationId = int(relations[i])
        direction = int(directions[i])  # pos for 1, neg for 0

        distmapPath = distmapDir + 'distmap_%i_%s.data' % (relationId, 'pos' if direction else 'neg')
        f = open(distmapPath, 'r')
        s = f.read().split('\n')
        f.close()

        keyEntities = s[0].split()
        valueEntities = s[1].split()

        relationEntityDistances.append(dict())
        startTiming(len(keyEntities))
        for i in range(len(keyEntities)):
            values = s[i + 2].split()
            assert len(valueEntities) == len(values)

            keyEntity = keyEntities[i]
            relationEntityDistances[-1][keyEntity] = []
            for j in range(len(valueEntities)):
                valueEntity = valueEntities[j]
                value = float(values[j])
                relationEntityDistances[-1][keyEntity].append((valueEntity, value))
            relationEntityDistances[-1][keyEntity].sort(key=lambda x: x[1])

            displayTiming()

        print('Relation = %i with direction = %i loaded, key entities = %i, value entities = %i.' %
              (relationId, direction, len(keyEntities), len(valueEntities)))

    print('Distances loaded.')

    return relationEntityDistances


def recommendCombinedRelation(relations, directions=None):
    def minDistModel():
        MAX = 10000000

        relationEntityDistances = loadRelationEntityDistances(relations, directions)
        num = len(relations)

        startTiming(len(entityList))
        for i in range(len(entityList)):
            minDistance = [dict() for i in range(num + 1)]
            minDistance[0][entityList[i]] = 0
            for j in range(num):
                for entityId in minDistance[j].keys():
                    distances = relationEntityDistances[j][entityId]
                    normalized = np.array([distances[i][1] for i in range(len(distances))])
                    normalized = (normalized - np.average(normalized)) / np.std(normalized)
                    for k in range(len(distances)):
                        recommendId = distances[k][0]
                        distance = normalized[k]
                        minDistance[j + 1][recommendId] = min(minDistance[j + 1].get(recommendId, MAX),
                                                              minDistance[j][entityId] + distance)

            outputProgress(minDistance[-1])

        del relationEntityDistances
        gc.collect()

    def outputProgress(distances):
        outputFile.write('%f' % distances[sortedEntityInfo[tailType][0]])
        for j in range(1, len(sortedEntityInfo[tailType])):
            recommendId = sortedEntityInfo[tailType][j]
            distance = distances[recommendId]
            outputFile.write(' %f' % distance)

        outputFile.write('\n')
        displayTiming()

    if directions is None:
        directions = [True] * len(relations)
    headType = relationHeads[relations[0]] if directions[0] else relationTails[relations[0]]
    tailType = relationTails[relations[-1]] if directions[-1] else relationHeads[relations[-1]]
    entityList = sortedEntityInfo[headType]

    outputPath = parentDir + '/res/%s/%s/%i/distmap/distmap_7_pos.data' % (database, method, order)
    outputFile = open(outputPath, 'w')
    outputFile.write(' '.join(sortedEntityInfo[headType]) + '\n')
    outputFile.write(' '.join(sortedEntityInfo[tailType]) + '\n')

    minDistModel()

    outputFile.close()


def testPaperInstitute():
    recommendCombinedRelation(relations=[2, 0], directions=[True, True])
    # recommendCombinedRelation(relations=[0, 2], directions=[False, False])


def test():
    testPaperInstitute()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method if parsedArgs.method else 'ComplEx_advanced'
order = parsedArgs.order if parsedArgs.order else 2

types = ['author', 'paper', 'field', 'venue', 'institute']
relationHeads = ['author', 'author', 'paper', 'paper', 'paper', 'paper', 'field']
relationTails = ['institute', 'field', 'author', 'field', 'venue', 'paper', 'field']

sortedEntityInfo = dict()
for typ in types:
    sortedEntityInfo[typ] = loadEntityInfo(typ)

test()
