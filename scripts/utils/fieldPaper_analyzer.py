from __future__ import print_function
from __future__ import division

import argparse
import os
import math
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


def output(f, s='', end='\n'):
    print(s + end, end='')
    if not f is None:
        f.write(s + end)


def outputMetric(logFile, metricString, metric, digit=4):
    output(logFile, metricString + ':', end=' ' * (24 - len(metricString)))
    for num in range(len(metric)):
        valueString = formattedRound(metric[num][0] / metric[num][1], digit)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)


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


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def averageValue(l):
    return sum(l) / len(l)


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


def loadPaperCitations():
    filePath = parentDir + '/data/%s/PaperCitations.data' % database
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    paperCitations = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 2:
            continue
        paperId = splited[0]
        citationCount = int(splited[1])
        paperCitations[paperId] = citationCount

    return paperCitations


def loadPaperYears():
    filePath = parentDir + '/data/%s/PaperYears.data' % database
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    paperYears = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 2:
            continue
        paperId = splited[0]
        year = int(splited[1])
        paperYears[paperId] = year

    return paperYears


def loadTriplets():
    filePath = parentDir + '/benchmarks/%s/triplets.txt' % database
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    triplets = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        headId = splited[0][1:]
        tailId = splited[2][1:]
        relationId = splited[1]

        if relationId == '3':
            addToSet(triplets, tailId, headId)

    return triplets


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--count', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
count = parsedArgs.count if parsedArgs.count is not None else 10

allDistances = loadRelationEntityDistances([3], [False])[0]
paperCitations = loadPaperCitations()
paperYears = loadPaperYears()
triplets = loadTriplets()

metrics = dict()
for metric in ['citation', 'log_citation', 'year']:
    metrics[metric] = [[0, 0] for i in range(count)]

startTiming(len(triplets))
for fieldId in triplets.keys():
    distances = allDistances[fieldId]
    paperIds = [distances[i][0] for i in range(len(distances)) if distances[i][0] in triplets[fieldId]]
    avgCitations = averageValue([paperCitations[paperId] for paperId in paperIds])
    avgLogCitations = averageValue([math.log(paperCitations[paperId]) for paperId in paperIds])
    avgYears = averageValue([paperYears[paperId] for paperId in paperIds])
    for i in range(min(count, len(paperIds))):
        paperId = paperIds[i]

        metrics['citation'][i][0] += paperCitations[paperId] - avgCitations
        metrics['citation'][i][1] += 1

        metrics['log_citation'][i][0] += math.log(paperCitations[paperId]) - avgLogCitations
        metrics['log_citation'][i][1] += 1

        metrics['year'][i][0] += paperYears[paperId] - avgYears
        metrics['year'][i][1] += 1

    displayTiming()

print(method)
print('-' * 50)
mkdir(['res', database, method, order, 'recommendation', 'analyzed'])
f = open(parentDir + '/res/%s/%s/%i/recommendation/analyzed/groundTruth_Recommend_analyzed.log' %
         (database, method, order), 'w')
for metric in ['citation', 'log_citation', 'year']:
    outputMetric(f, metric, metrics[metric])
    output(f)
f.close()
