import numpy as np

import argparse
import os
import codecs
import time

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

times = 0
timesTotal = 0
startTime = 0


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


def parseVector(vectorLine):
    splited = vectorLine.split('\t')
    try:
        return np.array([float(x) for x in splited])
    except:
        return np.array([complex(x) for x in splited])


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


def calcDistance(v1, v2):
    return np.sum(np.abs(v1 - v2))


def calcCosSimilarity(v1, v2):
    return -np.sum(v1 * v2)


def calcCosSimilarityForComplex(v1, v2):
    return -np.sum(np.real(v1 * np.conj(v2)))


def mapDistance(typ, relationId):
    print('Mapping distances for %ss...' % typ)

    f = open(parentDir + '/res/%s/%s/%i/%sVector.data' % (database, method, order, typ), 'r')
    s = f.read().split('\n')
    f.close()

    num = len(sortedEntityInfo[typ])
    vectors = []
    for i in range(num):
        vectors.append(parseVector(s[i]))

    startTiming(num)

    f = open(parentDir + '/res/%s/%s/%i/distmap/distmap_%s_pos.data' % (database, method, order, relationId), 'w')
    f.write(' '.join(sortedEntityInfo[typ]) + '\n')
    f.write(' '.join(sortedEntityInfo[typ]) + '\n')

    for i in range(num):
        f.write('%f' % (calc(vectors[i], vectors[0])))
        for j in range(1, num):
            f.write(' %f' % (calc(vectors[i], vectors[j])))
        f.write('\n')
        displayTiming()

    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method if parsedArgs.method else 'ComplEx_advanced'
order = parsedArgs.order if parsedArgs.order else 2

model = method.split('_')[0].lower()
if 'trans' in model:
    calc = calcDistance
elif 'distmult' in model:
    calc = calcCosSimilarity
elif 'complex' in model:
    calc = calcCosSimilarityForComplex
else:
    calc = calcDistance

types = ['paper', 'author', 'field', 'venue', 'institute']

sortedEntityInfo = dict()
for typ in types:
    sortedEntityInfo[typ] = loadEntityInfo(typ)

for i in range(len(types)):
    mapDistance(types[i], -i - 1)
