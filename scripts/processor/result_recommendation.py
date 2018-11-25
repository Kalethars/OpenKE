# Execution order:
# result_mapper -> pca_results_saver (optional) -> result_recommendation

import argparse
import os
import codecs

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


def parseVector(vectorLine):
    try:
        return list(map(lambda x: float(x), vectorLine.split('\t')))
    except:
        return list(map(lambda x: complex(x), vectorLine.split('\t')))


def calcDistance(v1, v2, norm):
    return sum([abs(v1[i] - v2[i]) ** norm for i in range(len(v1))])


def calcCosSimilarity(v1, v2, norm=None):
    return 1 - sum([v1[i] * v2[i] for i in range(len(v1))])


def calcCosSimilarityForComplex(v1, v2, norm=None):
    return 1 - sum([(v1[i] * v2[i].conjugate()).real for i in range(len(v1))])


def paperRecommendation():
    global outputPath

    name = dict()
    vectors = dict()

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1].strip()
        vectors[splited[0]] = parseVector(vectorLines[i])

    f = open(outputPath, 'w')
    print('Recommending papers...')
    print(len(vectors))

    sortedKeys = map(lambda x: x[0], sorted(name.items(), key=lambda x: x[1].lower()))

    count = 0
    for entityId in sortedKeys:
        count += 1
        if int(count * 100 / len(vectors)) > int((count - 1) * 100 / len(vectors)):
            print(str(int(count * 100 / len(vectors))) + '%')

        distance = dict()
        for entityId2 in vectors.keys():
            if entityId == entityId2:
                continue
            distance[entityId2] = calc(vectors[entityId], vectors[entityId2], norm)

        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def venueRecommendation():
    global outputPath

    name = dict()
    venueType = dict()
    category = dict()
    vectors = dict()

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        venueType[splited[0]] = splited[1]
        name[splited[0]] = splited[2].strip()
        category[splited[0]] = splited[3].replace('.', ' ')
        vectors[splited[0]] = parseVector(vectorLines[i])

    f = open(outputPath, 'w')
    print('Recommending venues...')
    print(len(vectors))

    sortedKeys = map(lambda x: x[0], sorted(name.items(), key=lambda x: x[1].lower()))

    count = 0
    for entityId in sortedKeys:
        count += 1
        if int(count * 100 / len(vectors)) > int((count - 1) * 100 / len(vectors)):
            print(str(int(count * 100 / len(vectors))) + '%')

        distance = dict()
        for entityId2 in vectors.keys():
            if entityId == entityId2:
                continue
            distance[entityId2] = calc(vectors[entityId], vectors[entityId2], norm)

        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] +
                '\t' + venueType[entityId] + '\t' + category[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] +
                    '\t' + venueType[sortedResults[i][0]] + '\t' + category[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def authorRecommendation():
    global outputPath

    f = open(parentDir + '/benchmarks/' + database + '/triplets.txt', 'r')
    s = f.read().split('\n')
    f.close()

    authorPaperCount = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        if splited[1] == '2':
            authorPaperCount[splited[2][1:]] = authorPaperCount.get(splited[2][1:], 0) + 1

    name = dict()
    vectors = dict()

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1].strip()
        vectors[splited[0]] = parseVector(vectorLines[i])

    f = open(outputPath, 'w')
    print('Recommending authors...')
    print(len(vectors))

    sortedKeys = map(lambda x: x[0], sorted(name.items(), key=lambda x: x[1].lower()))

    count = 0
    for entityId in sortedKeys:
        count += 1
        if int(count * 100 / len(vectors)) > int((count - 1) * 100 / len(vectors)):
            print(str(int(count * 100 / len(vectors))) + '%')

        distance = dict()
        for entityId2 in vectors.keys():
            if entityId == entityId2 or (limited and authorPaperCount.get(entityId2, 0) < 3):
                continue
            distance[entityId2] = calc(vectors[entityId], vectors[entityId2], norm)

        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def fieldRecommendation():
    global outputPath

    f = open(parentDir + '/benchmarks/' + database + '/triplets.txt', 'r')
    s = f.read().split('\n')
    f.close()

    fieldPaperCount = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        if splited[1] == '3':
            fieldPaperCount[splited[2][1:]] = fieldPaperCount.get(splited[2][1:], 0) + 1

    name = dict()
    vectors = dict()

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1].strip()
        vectors[splited[0]] = parseVector(vectorLines[i])

    f = open(outputPath, 'w')
    print('Recommending fields...')
    print(len(vectors))

    sortedKeys = map(lambda x: x[0], sorted(name.items(), key=lambda x: x[1].lower()))

    count = 0
    for entityId in sortedKeys:
        count += 1
        if int(count * 100 / len(vectors)) > int((count - 1) * 100 / len(vectors)):
            print(str(int(count * 100 / len(vectors))) + '%')

        distance = dict()
        for entityId2 in vectors.keys():
            if entityId == entityId2 or (limited and fieldPaperCount.get(entityId2, 0) < 5):
                continue
            distance[entityId2] = calc(vectors[entityId], vectors[entityId2], norm)

        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def instituteRecommendation():
    global outputPath

    f = open(parentDir + '/data/' + database + '/PaperAuthorAffiliations.data', 'r')
    s = f.read().split('\n')
    f.close()

    institutePapers = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 4:
            continue
        if institutePapers.get(splited[2], 0) == 0:
            institutePapers[splited[2]] = set()
        institutePapers[splited[2]].add(splited[0])

    institutePaperCount = dict()
    for entityId in institutePapers.keys():
        institutePaperCount[entityId] = len(institutePapers[entityId])

    name = dict()
    vectors = dict()

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1].strip()
        vectors[splited[0]] = parseVector(vectorLines[i])

    f = open(outputPath, 'w')
    print('Recommending institutes...')
    print(len(vectors))

    sortedKeys = map(lambda x: x[0], sorted(name.items(), key=lambda x: x[1].lower()))

    count = 0
    for entityId in sortedKeys:
        count += 1
        if int(count * 100 / len(vectors)) > int((count - 1) * 100 / len(vectors)):
            print(str(int(count * 100 / len(vectors))) + '%')

        distance = dict()
        for entityId2 in vectors.keys():
            if entityId == entityId2 or (limited and institutePaperCount.get(entityId2, 0) < 5):
                continue
            distance[entityId2] = calc(vectors[entityId], vectors[entityId2], norm)

        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--count', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--pca', type=bool, required=False)
parser.add_argument('--norm', type=float, required=False)
parser.add_argument('--unlimited', type=bool, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
update = parsedArgs.update if parsedArgs.update else False
recommendCount = parsedArgs.count if parsedArgs.count and parsedArgs.count > 10 else 10
target = parsedArgs.target
pca = parsedArgs.pca if parsedArgs.pca else False
norm = parsedArgs.norm if parsedArgs.norm else (2 if pca else 1)
limited = not (parsedArgs.unlimited if parsedArgs.unlimited else False)

model = method.split('_')[0].lower()
if 'trans' in model:
    calc = calcDistance
elif model == 'distmult':
    calc = calcCosSimilarity
elif model == 'complex':
    calc = calcCosSimilarityForComplex
else:
    calc = calcDistance

types = ['paper', 'author', 'institute', 'field', 'venue']

for typ in types:
    if target and typ != target:
        continue
    infoReadDir = parentDir + '/data/' + database + '/info/'
    vectorReadDir = parentDir + '/res/' + '/'.join([database, method, str(order)]) + '/'
    recommendationDir = vectorReadDir + 'recommendation/'

    outputPath = recommendationDir + typ + 'Recommendation' + \
                 '_norm=' + str(round(norm, 2)).rstrip('.0') + \
                 ('_PCA' if pca else '') + \
                 ('' if limited else '_unlimited') + '.txt'
    if not update:
        if os.path.exists(outputPath):
            continue
    if not os.path.exists(recommendationDir):
        os.mkdir(recommendationDir)

    f = codecs.open(infoReadDir + typ + 'Info.data', 'r', 'gbk')
    infoLines = f.read().split('\n')
    f.close()

    if pca:
        f = open(vectorReadDir + 'pca/' + typ + 'PCA.data', 'r')
    else:
        f = open(vectorReadDir + typ + 'Vector.data', 'r')
    vectorLines = f.read().split('\n')
    f.close()

    exec(typ + 'Recommendation()')
