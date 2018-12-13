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
        f = codecs.open(analyzedLogPath, 'r', 'utf-8')
        s = f.read().split('\n')
        f.close()

        bestOrder = int(s[1].split()[1])
        return bestOrder
    except:
        return 1


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def normalize(data):
    values = np.array([x[1] for x in data])
    values = (values - np.average(values)) / np.std(values)
    return [(data[i][0], values[i]) for i in range(len(data))]


def loadEntityList(typ):
    typeEntityCount = dict()
    if typ == 'field':
        f = open(parentDir + '/benchmarks/%s/triplets.txt' % database, 'r')
        s = f.read().split('\n')
        f.close()

        for line in s:
            splited = line.split()
            if len(splited) == 3 and splited[1] in {'1', '3'}:
                typeEntityCount[splited[2][1:]] = typeEntityCount.get(splited[2][1:], 0) + 1

    f = codecs.open(parentDir + '/data/%s/info/%sInfo.data' % (database, typ), 'r', encoding='utf-8', errors='ignore')
    infoLines = f.read().split('\n')
    f.close()

    entityInfo = dict()
    typeEntityList = []
    for i in range(len(infoLines)):
        splited = infoLines[i].split('\t')
        if typ != 'venue':
            if len(splited) != 2:
                continue
            entityId = splited[0]
            info = splited[1]
        else:
            if len(splited) != 5:
                continue
            entityId = splited[0]
            info = splited[2]
        if typ == 'field' and typeEntityCount.get(entityId, 0) <= 2:
            continue
        else:
            typeEntityList.append(entityId)
        entityInfo[entityId] = info.encode('utf-8').decode('ascii', 'ignore').strip()

    return entityInfo, typeEntityList


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
            distances = []
            for j in range(len(valueEntities)):
                valueEntity = valueEntities[j]
                value = float(values[j])
                distances.append((valueEntity, value))

            distances.sort(key=lambda x: x[1])
            distances = normalize(distances)

            relationEntityDistances[-1][keyEntity] = dict()
            for (valueEntity, value) in distances:
                relationEntityDistances[-1][keyEntity][valueEntity] = value
            for (valueEntity, value) in distances:
                if valueEntity not in relationEntityDistances[-1][keyEntity]:
                    relationEntityDistances[-1][keyEntity][valueEntity] = distances[-1][1]

            displayTiming()

        print('Relation = %i with direction = %i loaded, key entities = %i, value entities = %i.' %
              (relationId, direction, len(keyEntities), len(valueEntities)))

    print('Distances loaded.')

    return relationEntityDistances


def analyzeQuery(query):
    matched = []
    partially = False
    remain = 1
    query = query.strip()

    if '?' in query:
        partially = True
        try:
            remain = int(query.split('?')[1])
        except:
            remain = 1
        query = query.split('?')[0]
    for (info, typ, entityId) in reverseInfo:
        if partially:
            if query.lower() in info:
                matched.append((info, typ, entityId, (len(query) - 1) / len(info)))
        else:
            if query.lower() == info or query.upper() == entityId:
                matched.append((info, typ, entityId, 1))

    matched.sort(key=lambda x: x[3], reverse=True)
    if partially and remain < len(matched):
        del matched[remain:]

    return matched


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--target', type=str, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method if parsedArgs.method else 'ComplEx_advanced'
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
update = parsedArgs.update if parsedArgs.update else False
target = parsedArgs.target.lower() if parsedArgs.target is not None else 'paper'

relationVectors = []
normalVectors = []

types = ['author', 'paper', 'field', 'venue', 'institute']
relationHeads = ['author', 'author', 'paper', 'paper', 'paper', 'paper', 'field']
relationTails = ['institute', 'field', 'author', 'field', 'venue', 'paper', 'field']

entityInfo = dict()
typeEntityList = dict()
for typ in types:
    entityInfo[typ], typeEntityList[typ] = loadEntityList(typ)

# 0: author_institute, 1: author_field, 2: paper_author
# 3: paper_field, 4: paper_venue
# 7: paper_institute, 8: venue_field, 9: author_venue
# -1: paper, -2: author, -3: field, -4: venue, -5: institute
if target == 'paper':
    relationsEntityDistances = loadRelationEntityDistances([2, 3, 4, 7, -1], [True, True, True, True, True])
    typeRelationMap = {'author': 0, 'field': 1, 'venue': 2, 'institute': 3, 'paper': 4}
elif target == 'venue':
    relationsEntityDistances = loadRelationEntityDistances([4, 8, 9, -4], [False, True, False, True])
    typeRelationMap = {'paper': 0, 'field': 1, 'author': 2, 'venue': 3}
elif target == 'field':
    relationsEntityDistances = loadRelationEntityDistances([1, 3, 8, -3], [False, False, False, True])
    typeRelationMap = {'author': 0, 'paper': 1, 'venue': 2, 'field': 3}
elif target == 'author':
    relationsEntityDistances = loadRelationEntityDistances([0, 1, 2, 9, -2], [True, True, False, True, True])
    typeRelationMap = {'institute': 0, 'field': 1, 'paper': 2, 'venue': 3, 'author': 4}
else:
    raise ValueError('Invalid target!')

reverseInfo = []
for typ in types:
    if typ in typeRelationMap:
        for entityId in entityInfo[typ].keys():
            reverseInfo.append((entityInfo[typ][entityId].lower(), typ, entityId))

while True:
    queries = input('Query: ')
    if queries == '#':
        break
    queries = list(map(lambda x: x.strip(), queries.split(',')))
    analyzedQuery = []
    for query in queries:
        matched = []
        for q in query.split('|'):
            matched += analyzeQuery(q)

        print('Matched for %s:' % query, end='')
        for i in range(len(matched)):
            print('\t(%s)' % ', '.join(matched[i][:3]), end='')
        print()

        analyzedQuery.append((query, [(x[2], x[1]) for x in matched]))

    maxValue = 1000000
    if len(analyzedQuery) > 0:
        contribution = dict()
        contributor = dict()
        for candidateId in typeEntityList[target]:
            contribution[candidateId] = dict()
            contributor[candidateId] = dict()

        resultDistances = dict()
        fullScore = 0
        for i in range(len(analyzedQuery)):
            if len(analyzedQuery[i][1]) == 0:
                continue

            localDistances = dict()
            localEntities = dict()
            query = analyzedQuery[i][0]
            for candidateId in typeEntityList[target]:
                for (entityId, typ) in analyzedQuery[i][1]:
                    distance = relationsEntityDistances[typeRelationMap[typ]][candidateId].get(entityId, maxValue)
                    if distance < localDistances.get(candidateId, maxValue):
                        localDistances[candidateId] = distance
                        localEntities[candidateId] = (entityId, typ)
            queryFullScore = min(localDistances.values())
            fullScore += queryFullScore
            for candidateId in typeEntityList[target]:
                resultDistances[candidateId] = resultDistances.get(candidateId, 0) + localDistances[candidateId]
                contribution[candidateId][query] = localDistances[candidateId] / queryFullScore * 100
                contributor[candidateId][query] = \
                    entityInfo[localEntities[candidateId][1]][localEntities[candidateId][0]]

            del localDistances
            del localEntities

        results = sorted(resultDistances.keys(), key=lambda x: resultDistances[x])
        for i in range(min(10, len(results))):
            print('%i\t%s\t%s' % (i + 1, results[i], entityInfo[target][results[i]]))

            distance = resultDistances[results[i]]
            print('\tScore: %.1f' % (distance / fullScore * 100), end='')
            for j in range(len(analyzedQuery)):
                if len(analyzedQuery[j][1]) == 0:
                    continue
                query = analyzedQuery[j][0]
                print('\t%s: %.1f' % (contributor[results[i]][query], contribution[results[i]][query]), end='')
            print()

        del resultDistances
        del contribution
        del contributor
        gc.collect()
