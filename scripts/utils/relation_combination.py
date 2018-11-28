import argparse
import os

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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


def recommendCombinedRelation(model, relations, directions=None):
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

    def validate():
        if len(relations) != len(directions):
            raise ValueError('Relations and directions must have the same length!')
        for i in range(len(relations) - 1):
            tailType = relationTails[relations[i]] if directions[i] else relationHeads[relations[i]]
            headType = relationHeads[relations[i + 1]] if directions[i + 1] else relationTails[relations[i + 1]]
            if tailType != headType:
                raise ValueError('Relations not matched!')

    if directions is None:
        directions = [True] * len(relations)
    validate()
    headType = relationHeads[relations[0]] if directions[0] else relationTails[relations[0]]
    tailType = relationTails[relations[-1]] if directions[-1] else relationHeads[relations[-1]]

    outputPath = parentDir + '/res/%s/%s/%i/recommendation/combinedRecommendation_%s_%s.txt' % \
                 (database, method, order, headType, tailType)
    if (not update) and (recommendCount > 0) and os.path.exists(outputPath):
        return

    entityList = sortedEntityInfo[headType]
    vectors = entityVectors[headType]

    total = 0
    print('Recommending %s for %s...' % (tailType, headType))
    print(len(entityList))

    if recommendCount > 0:
        f = open(outputPath, 'w')
    else:
        recommendResults = dict()
    for i in range(len(entityList)):
        entityId = entityList[i]
        entityVector = vectors[entityId]
        for j in range(len(relations)):
            relationVector = getRelationVector(relations[j], directions[j])
            entityVector = applyRelation(transfer(entityVector, relations[j]), relationVector)

        distance = dict()
        for recommendId in entityVectors[tailType].keys():
            recommendVector = transfer(entityVectors[tailType][recommendId], relations[-1])
            distance[recommendId] = calcDistance(entityVector, recommendVector)
        sortedDistance = sorted(distance.keys(), key=lambda x: distance[x])

        if recommendCount > 0:
            f.write('Recommend: %s - %s\n' % (entityId, entityInfo[headType][entityId]))
            f.write('-' * 50 + '\n')
            for j in range(recommendCount):
                recommendId = sortedDistance[j]
                f.write('%s\t%s\n' % (recommendId, entityInfo[tailType][recommendId]))
            f.write('\n')
        else:
            recommendResults[entityId] = sortedDistance

        total += 1
        if int(total * 100 / len(entityList)) > int((total - 1) * 100 / len(entityList)):
            print(str(int(total * 100 / len(entityList))) + '%')

    if recommendCount > 0:
        f.close()
        return
    else:
        return recommendResults


def loadPaperInstitute():
    global paperInstitute, institutePaper

    f = open(parentDir + '/data/%s/paperAuthorAffiliations.data' % database, 'r')
    s = f.read().split('\n')
    f.close()

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


def testVenueField():
    recommendCombinedRelation(model, relations=[4, 3], directions=[False, True])
    recommendCombinedRelation(model, relations=[3, 4], directions=[False, True])


def testAuthorVenue():
    recommendCombinedRelation(model, relations=[2, 4], directions=[False, True])
    recommendCombinedRelation(model, relations=[4, 2], directions=[False, True])


def testPaperInstitute():
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

        f.write('Predict %s for %s:\n' % (headType, tailType))
        f.write('MRR:\t%f\n' % (meanReciprocalRank))
        for num in hitAt:
            f.write('Hit@%i:\t%f\n' % (num, hitAtValue[num]))
        f.write('Score:\t%f\n' % (meanReciprocalRank * sum(hitAtValue.values()) / len(hitAtValue)))
        f.write('\n')

        f.close()

    if recommendCount <= 0:
        global paperInstitute, institutePaper

    paperInstituteResults = recommendCombinedRelation(model, relations=[2, 0], directions=[True, True])
    if recommendCount <= 0:
        testLinkPrediction(paperInstitute, paperInstituteResults, 'institute', 'paper')

    institutePaperResults = recommendCombinedRelation(model, relations=[0, 2], directions=[False, False])
    if recommendCount <= 0:
        testLinkPrediction(institutePaper, institutePaperResults, 'paper', 'institute')


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
parser.add_argument('--count', type=int, required=False)
parser.add_argument('--update', type=bool, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
recommendCount = parsedArgs.count if parsedArgs.count is not None else 10  # if recommendCount <= 0, test link prediction
update = parsedArgs.update if parsedArgs.update else False

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
    f = open(parentDir + '/data/%s/info/%sInfo.data' % (database, typ), 'r')
    infoLines = f.read().split('\n')
    f.close()

    f = open(parentDir + '/res/%s/%s/%i/%sVector.data' % (database, method, order, typ), 'r')
    vectorLines = f.read().split('\n')
    f.close()

    entityInfo[typ] = dict()
    entityVectors[typ] = dict()
    for i in range(len(infoLines)):
        splited = infoLines[i].split('\t')
        if typ != 'venue':
            if len(splited) != 2:
                continue
            entityId = splited[0]
            entityInfo[typ][entityId] = splited[1]
        else:
            if len(splited) != 5:
                continue
            entityId = splited[0]
            entityInfo[typ][entityId] = splited[2] + '\t' + splited[3].replace('.', ' ')

        splited = vectorLines[i].split()
        if len(splited) < 2:
            continue
        try:
            entityVectors[typ][entityId] = list(map(lambda x: float(x), splited))
        except:
            entityVectors[typ][entityId] = list(map(lambda x: complex(x), splited))

    sortedEntityInfo[typ] = sorted(entityInfo[typ].keys(), key=lambda x: entityInfo[typ][x])

if recommendCount <= 0:
    paperInstitute = dict()
    institutePaper = dict()
    loadPaperInstitute()

    testResultLog = parentDir + '/res/%s/%s/%i/recommendation/analyzed/combined_recommendation_analysis.log' % \
                    (database, method, order)
    f = open(testResultLog, 'w')
    f.close()
test()
