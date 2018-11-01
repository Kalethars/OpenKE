# Execution order:
# result_mapper -> pca_results_saver -> result_recommendation

import argparse
import os


def paperRecommendation():
    global outputPath, infoLines, vectorLines, recommendCount

    name = dict()
    vectors = dict()
    dimension = len(vectorLines[0].split('\t'))

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1]
        vectors[splited[0]] = list(map(lambda x: float(x), vectorLines[i].split('\t')))

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
            distance[entityId2] = \
                sum([(vectors[entityId][i] - vectors[entityId2][i]) ** 2 for i in range(dimension)])
        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def venueRecommendation():
    global outputPath, infoLines, vectorLines, recommendCount

    name = dict()
    venueType = dict()
    category = dict()
    vectors = dict()
    dimension = len(vectorLines[0].split('\t'))

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        venueType[splited[0]] = splited[1]
        name[splited[0]] = splited[2]
        category[splited[0]] = splited[3].replace('.', ' ')
        vectors[splited[0]] = list(map(lambda x: float(x), vectorLines[i].split('\t')))

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
            distance[entityId2] = \
                sum([(vectors[entityId][i] - vectors[entityId2][i]) ** 2 for i in range(dimension)])
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
    global outputPath, infoLines, vectorLines, recommendCount

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
    dimension = len(vectorLines[0].split('\t'))

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1]
        vectors[splited[0]] = list(map(lambda x: float(x), vectorLines[i].split('\t')))

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
            if entityId == entityId2 or authorPaperCount.get(entityId2, 0) < 3:
                continue
            distance[entityId2] = \
                sum([(vectors[entityId][i] - vectors[entityId2][i]) ** 2 for i in range(dimension)])
        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def fieldRecommendation():
    global outputPath, infoLines, vectorLines, recommendCount

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
    dimension = len(vectorLines[0].split('\t'))

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1]
        vectors[splited[0]] = list(map(lambda x: float(x), vectorLines[i].split('\t')))

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
            if entityId == entityId2 or fieldPaperCount.get(entityId2, 0) < 5:
                continue
            distance[entityId2] = \
                sum([(vectors[entityId][i] - vectors[entityId2][i]) ** 2 for i in range(dimension)])
        sortedResults = sorted(distance.items(), key=lambda x: x[1])
        f.write('Recommend: ' + entityId + ' - ' + name[entityId] + '\n')
        f.write('-' * 50 + '\n')
        for i in range(recommendCount):
            f.write(sortedResults[i][0] + '\t' + name[sortedResults[i][0]] + '\n')
        f.write('\n')
    f.close()


def instituteRecommendation():
    global outputPath, infoLines, vectorLines, recommendCount

    f = open(parentDir + '/data/' + database + '/PaperAuthorAffiliations.data', 'r')
    s = f.read().split('\n')
    f.close()

    institutePaper = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 4:
            continue
        if institutePaper.get(splited[2], 0) == 0:
            institutePaper[splited[2]] = set()
        institutePaper[splited[2]].add(splited[0])

    institutePaperCount = dict()
    for entityId in institutePaper.keys():
        institutePaperCount[entityId] = len(institutePaper[entityId])

    name = dict()
    vectors = dict()
    dimension = len(vectorLines[0].split('\t'))

    for i in range(len(infoLines) - 1):
        splited = infoLines[i].split('\t')
        name[splited[0]] = splited[1]
        vectors[splited[0]] = list(map(lambda x: float(x), vectorLines[i].split('\t')))

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
            if entityId == entityId2 or institutePaperCount.get(entityId2, 0) < 5:
                continue
            distance[entityId2] = \
                sum([(vectors[entityId][i] - vectors[entityId2][i]) ** 2 for i in range(dimension)])
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
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--count', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order
update = parsedArgs.update if parsedArgs.update else False
recommendCount = parsedArgs.count if parsedArgs.count and parsedArgs.count > 10 else 10
target = parsedArgs.target

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

types = ['paper', 'author', 'institute', 'field', 'venue']

for type in types:
    if target and type != target:
        continue
    infoReadDir = parentDir + '/data/' + database + '/info/'
    vectorReadDir = parentDir + '/res/' + '/'.join([database, method, str(order)]) + '/'

    outputPath = vectorReadDir + type + 'Recommendation.txt'
    if not update:
        if os.path.exists(outputPath):
            continue

    f = open(infoReadDir + type + 'Info.data', 'r')
    infoLines = f.read().split('\n')
    f.close()

    f = open(vectorReadDir + type + 'Vector.data', 'r')
    vectorLines = f.read().split('\n')
    f.close()

    exec(type + 'Recommendation()')
