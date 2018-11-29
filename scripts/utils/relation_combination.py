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


def startTiming(total):
    global times, timesTotal, startTime

    times = 0
    startTime = time.time()
    timesTotal = total

    print(timesTotal)


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


def loadEntityInfo(typ, entityInfo, entityVectors, sortedEntityInfo):
    f = codecs.open(parentDir + '/data/%s/info/%sInfo.data' % (database, typ), 'r', encoding='utf-8', errors='ignore')
    infoLines = f.read().split('\n')
    f.close()
    entityInfo[typ] = dict()

    if algorithm == 'chained':
        f = open(parentDir + '/res/%s/%s/%i/%sVector.data' % (database, method, order, typ), 'r')
        vectorLines = f.read().split('\n')
        f.close()
        entityVectors[typ] = dict()

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
            info = splited[2] + '\t' + splited[3].replace('.', ' ')
        entityInfo[typ][entityId] = info.encode('utf-8').decode('ascii', 'ignore').strip()

        if algorithm == 'chained':
            splited = vectorLines[i].split()
            if len(splited) < 2:
                continue
            try:
                entityVectors[typ][entityId] = list(map(lambda x: float(x), splited))
            except:
                entityVectors[typ][entityId] = list(map(lambda x: complex(x), splited))

    sortedEntityInfo[typ] = sorted(entityInfo[typ].keys(), key=lambda x: entityInfo[typ][x])


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
        for i in range(len(keyEntities)):
            values = s[i + 2].split()
            assert len(valueEntities) == len(values)

            keyEntity = keyEntities[i]
            relationEntityDistances[-1][keyEntity] = []
            for j in range(len(valueEntities)):
                valueEntity = valueEntities[j]
                value = float(values[j])
                relationEntityDistances[-1][keyEntity].append((valueEntity, value))

        print('Relation = %i with direction = %i loaded, key entities = %i, value entities = %i.' %
              (relationId, direction, len(keyEntities), len(valueEntities)))

    print('Distances loaded.')

    return relationEntityDistances


def loadTypeConstraint():
    f = open(parentDir + '/benchmarks/%s/triplets.txt' % database, 'r')
    s = f.read().split('\n')
    f.close()

    typeConstraint = [dict(), dict()]
    for line in s:
        splited = line.split()
        if len(splited) == 3:
            headId = splited[0][1:]
            relationId = int(splited[1])
            tailId = splited[2][1:]

            addToSet(typeConstraint[0], relationId, headId)
            addToSet(typeConstraint[1], relationId, tailId)

    return typeConstraint


def recommendCombinedRelation(model, algorithm, relations, directions=None):
    def getRelationVector(relation, direction):
        if direction or model in {'distmult'}:
            return relationVectors[relation]
        elif model in {'complex'}:
            return [x.conjugate() for x in relationVectors[relation]]
        elif model in {'transe', 'transh'}:
            return [-x for x in relationVectors[relation]]
        else:
            raise ValueError('Invalid model!')

    def calcDistance(v1, v2):
        if model in {'transe', 'transh'}:
            return sum([abs(v1[i] - v2[i]) for i in range(len(v1))])
        elif model == 'distmult':
            return -sum([v1[i] * v2[i] for i in range(len(v1))])
        elif model == 'complex':
            return -sum([(v1[i] * v2[i].conjugate()).real for i in range(len(v1))])
        else:
            raise ValueError('Invalid model!')

    def applyRelation(e, r):
        if model in {'transe', 'transh'}:
            return [e[i] + r[i] for i in range(len(e))]
        elif model in {'distmult', 'complex'}:
            return [e[i] * r[i] for i in range(len(e))]
        else:
            raise ValueError('Invalid model!')

    def transfer(v, r):
        if model != 'transh':
            return v
        n = normalVectors[r]
        s = sum(v[i] * n[i] for i in range(len(v)))
        return [v[i] - s * n[i] for i in range(len(v))]

    def available(entityId, relation, direction):
        return entityId in typeConstraint[direction][relation]

    def validate():
        if len(relations) != len(directions):
            raise ValueError('Relations and directions must have the same length!')
        for i in range(len(relations) - 1):
            tailType = relationTails[relations[i]] if directions[i] else relationHeads[relations[i]]
            headType = relationHeads[relations[i + 1]] if directions[i + 1] else relationTails[relations[i + 1]]
            if tailType != headType:
                raise ValueError('Relations not matched!')

    def chainedModel():
        startTiming(len(entityList))

        vectors = entityVectors[headType]
        for i in range(len(entityList)):
            entityId = entityList[i]
            entityVector = vectors[entityId]
            for j in range(len(relations)):
                relationVector = getRelationVector(relations[j], directions[j])
                entityVector = applyRelation(transfer(entityVector, relations[j]), relationVector)

            distances = dict()
            for recommendId in entityVectors[tailType].keys():
                if not available(recommendId, relations[-1], directions[-1]):
                    continue
                recommendVector = transfer(entityVectors[tailType][recommendId], relations[-1])
                distances[recommendId] = calcDistance(entityVector, recommendVector)
            sortedDistances = sorted(distances.keys(), key=lambda x: distances[x])

            if recommendCount > 0:
                f.write('Recommend: %s - %s\n' % (entityId, entityInfo[headType][entityId]))
                f.write('-' * 50 + '\n')
                for j in range(recommendCount):
                    recommendId = sortedDistances[j]
                    f.write('%s\t%s\n' % (recommendId, entityInfo[tailType][recommendId]))
                f.write('\n')
            else:
                recommendResults[entityId] = sortedDistances

            displayTiming()

    def minDistModel():
        startTiming(len(entityList))
        MAX = 10000000

        relationEntityDistances = loadRelationEntityDistances(relations, directions)
        num = len(relations)

        for i in range(len(entityList)):
            minDistance = [dict() for i in range(num + 1)]
            minDistance[0][entityList[i]] = 0
            for j in range(num):
                for entityId in minDistance[j].keys():
                    distances = relationEntityDistances[j][entityId]
                    for (recommendId, distance) in distances:
                        if j == num - 1:
                            if not available(recommendId, relations[-1], directions[-1]):
                                continue
                        minDistance[j + 1][recommendId] = min(minDistance[j + 1].get(recommendId, MAX),
                                                              minDistance[j][entityId] + distance)

            distances = minDistance[-1]
            sortedDistances = sorted(distances.keys(), key=lambda x: distances[x])

            entityId = entityList[i]
            if recommendCount > 0:
                f.write('Recommend: %s - %s\n' % (entityId, entityInfo[headType][entityId]))
                f.write('-' * 50 + '\n')
                for j in range(recommendCount):
                    recommendId = sortedDistances[j]
                    f.write('%s\t%s\n' % (recommendId, entityInfo[tailType][recommendId]))
                f.write('\n')
            else:
                recommendResults[entityId] = sortedDistances

            displayTiming()

        del relationEntityDistances
        gc.collect()

    if directions is None:
        directions = [True] * len(relations)
    validate()
    headType = relationHeads[relations[0]] if directions[0] else relationTails[relations[0]]
    tailType = relationTails[relations[-1]] if directions[-1] else relationHeads[relations[-1]]

    outputPath = parentDir + '/res/%s/%s/%i/recommendation/%s_recommendation_%s_%s.txt' % \
                 (database, method, order, algorithm, headType, tailType)
    if (not update) and (recommendCount > 0) and os.path.exists(outputPath):
        return

    entityList = sortedEntityInfo[headType]

    print('Recommending %s for %s...' % (tailType, headType))

    if recommendCount > 0:
        f = open(outputPath, 'w')
    else:
        recommendResults = dict()

    if algorithm == 'chained':
        chainedModel()
    elif algorithm == 'mindist':
        minDistModel()

    if recommendCount > 0:
        f.close()
        return
    else:
        return recommendResults


def loadAuthorVenue():
    f = open(parentDir + '/benchmarks/%s/triplets.txt' % database, 'r')
    s = f.read().split('\n')
    f.close()

    paperAuthor = dict()
    paperVenue = dict()
    authorVenue = dict()
    venueAuthor = dict()
    for line in s:
        splited = line.split()
        if len(splited) == 3:
            headId = splited[0][1:]
            relationId = splited[1]
            tailId = splited[2][1:]

            if relationId == '2':
                addToSet(paperAuthor, headId, tailId)
            elif relationId == '4':
                addToSet(paperVenue, headId, tailId)

    for paperId in paperAuthor.keys():
        for authorId in paperAuthor[paperId]:
            for venueId in paperVenue.get(paperId, set()):
                addToSet(authorVenue, authorId, venueId)
                addToSet(venueAuthor, venueId, authorId)

    return authorVenue, venueAuthor


def loadPaperInstitute():
    f = open(parentDir + '/data/%s/PaperAuthorAffiliations.data' % database, 'r')
    s = f.read().split('\n')
    f.close()

    paperInstitute = dict()
    institutePaper = dict()
    for line in s:
        splited = line.split('\t')
        if len(splited) != 4:
            continue
        if len(splited[2]) != 8:
            continue
        paperId = splited[0]
        instituteId = splited[2]
        if not paperId in paperInstitute:
            paperInstitute[paperId] = set()
        paperInstitute[paperId].add(instituteId)
        if not instituteId in institutePaper:
            institutePaper[instituteId] = set()
        institutePaper[instituteId].add(paperId)

    return paperInstitute, institutePaper


def testLinkPrediction(groundTruth, predicted, headType, tailType):
    global testResultLog
    f = open(testResultLog, 'a')

    hitAt = [10, 3, 1]
    meanReciprocalRank = 0
    hitAtValue = dict()
    for num in hitAt:
        hitAtValue[num] = 0

    total = 0
    for headId in groundTruth.keys():
        total += len(groundTruth[headId])

        rank = dict()
        found = dict()
        for tailId in groundTruth[headId]:
            rank[tailId] = -1
            found[tailId] = False

        cnt = 1
        for predictId in predicted.get(headId, []):
            if not predictId in groundTruth[headId]:
                cnt += 1
            else:
                rank[predictId] = cnt

        for tailId in groundTruth[headId]:
            meanReciprocalRank += 1 / rank[tailId]
            for num in hitAt:
                if rank[tailId] <= num:
                    hitAtValue[num] += 1

    meanReciprocalRank /= total
    for num in hitAt:
        hitAtValue[num] /= total

    f.write('Predict %s for %s:\n' % (tailType, headType))
    f.write('MRR:\t%f\n' % (meanReciprocalRank))
    for num in hitAt:
        f.write('Hit@%i:\t%f\n' % (num, hitAtValue[num]))
    f.write('Score:\t%f\n' % (meanReciprocalRank * sum(hitAtValue.values()) / len(hitAtValue)))
    f.write('\n')

    f.close()


def testVenueField():
    recommendCombinedRelation(model, algorithm, relations=[4, 3], directions=[False, True])
    recommendCombinedRelation(model, algorithm, relations=[3, 4], directions=[False, True])


def testAuthorVenue():
    if recommendCount <= 0:
        authorVenue, venueAuthor = loadAuthorVenue()

    authorVenueResults = recommendCombinedRelation(model, algorithm, relations=[2, 4], directions=[False, True])
    if recommendCount <= 0:
        testLinkPrediction(authorVenue, authorVenueResults, 'author', 'venue')

    venueAuthorResults = recommendCombinedRelation(model, algorithm, relations=[4, 2], directions=[False, True])
    if recommendCount <= 0:
        testLinkPrediction(venueAuthor, venueAuthorResults, 'venue', 'author')


def testPaperInstitute():
    if recommendCount <= 0:
        paperInstitute, institutePaper = loadPaperInstitute()

    paperInstituteResults = recommendCombinedRelation(model, algorithm, relations=[2, 0], directions=[True, True])
    if recommendCount <= 0:
        testLinkPrediction(paperInstitute, paperInstituteResults, 'paper', 'institute')

    institutePaperResults = recommendCombinedRelation(model, algorithm, relations=[0, 2], directions=[False, False])
    if recommendCount <= 0:
        testLinkPrediction(institutePaper, institutePaperResults, 'institute', 'paper')


def test():
    if recommendCount > 0:
        # Predict field for venue, combine relation 4 (paper_is_published_on_venue) and relation 3 (paper_is_in_field)
        testVenueField()
    # Predict venue for author, combine relation 2 (paper_is_written_by_author) and relation 4 (paper_is_published_on_venue)
    testAuthorVenue()
    # Predict paper for institute, combine relation 2 (paper_is_written_by_author) and relation 0 (author_work_in_institute)
    testPaperInstitute()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--count', type=int, required=False)  # set count <= 0 to launch link prediction test
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--alg', type=str, required=False)  # 'chained' or 'mindist'
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
recommendCount = parsedArgs.count if parsedArgs.count is not None else 10
update = parsedArgs.update if parsedArgs.update else False
algorithm = parsedArgs.alg.lower() if parsedArgs.alg else 'chained'

if 'transe' in method.lower():
    model = 'transe'
elif 'transh' in method.lower():
    model = 'transh'
elif 'distmult' in method.lower():
    model = 'distmult'
elif 'complex' in method.lower():
    model = 'complex'
else:
    raise ValueError('Invalid model!')

if not algorithm in ['chained', 'mindist']:
    raise ValueError('Invalid algorithm!')

f = open(parentDir + '/res/%s/%s/%i/relationVector.data' % (database, method, order), 'r')
s = f.read().split('\n')
f.close()

relationVectors = []
for line in s:
    splited = line.split()
    if len(splited) < 2:
        continue
    try:
        relationVectors.append(list(map(lambda x: float(x), splited)))
    except:
        relationVectors.append(list(map(lambda x: complex(x), splited)))

normalVectors = []
if model == 'transh':
    for line in s:
        splited = line.split()
        if len(splited) < 2:
            continue
        normalVectors.append(list(map(lambda x: float(x), splited)))

types = ['author', 'paper', 'field', 'venue', 'institute']
relationHeads = ['author', 'author', 'paper', 'paper', 'paper', 'paper', 'field']
relationTails = ['institute', 'field', 'author', 'field', 'venue', 'paper', 'field']

entityInfo = dict()
entityVectors = dict()
sortedEntityInfo = dict()
for typ in types:
    loadEntityInfo(typ, entityInfo, entityVectors, sortedEntityInfo)
typeConstraint = loadTypeConstraint()

if recommendCount <= 0:
    testResultLog = parentDir + '/res/%s/%s/%i/recommendation/analyzed/%s_recommendation_analysis.log' % \
                    (database, method, order, algorithm)
    mkdir(['res', database, method, order, 'recommendation', 'analyzed'])
    f = open(testResultLog, 'w')
    f.close()

test()
