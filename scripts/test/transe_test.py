import argparse
import os
import gc
import win_unicode_console

win_unicode_console.enable()


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def entityInfo(entity):
    return typeIndex.get(entity, '_')[0] + entity + \
           '(' + str(idIndex[entity]) + ')' + ' ' * (len(str(entityNum)) - len(str(idIndex[entity])))


def output(f, s='', end='\n'):
    print(str(s) + end, end='')
    f.write(str(s) + end)


parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--superfilter', type=bool, required=False)
parser.add_argument('--pca', type=int, required=False)
parser.add_argument('--norm', type=float, required=False)
parser.add_argument('--test', type=str, required=False)
parsedConfig = parser.parse_args()

dataset = parsedConfig.dataset if parsedConfig.dataset else 'ACE17K'
method = parsedConfig.method if parsedConfig.method else 'TransE'
order = parsedConfig.order
superFilter = parsedConfig.superfilter if parsedConfig.superfilter else False
norm = parsedConfig.norm if parsedConfig.norm else 1
testString = parsedConfig.test

if testString != None:
    splited = testString.split()
    if len(splited) != 3:
        raise ValueError('Test format error! Must be like "head tail relation".')
    for i in range(len(splited)):
        try:
            int(splited[i])
        except:
            raise ValueError('Test format error! Please input number id!')

types = ['paper', 'author', 'institute', 'field', 'venue']
typeMap = {'p': 'paper', 'a': 'author', 'i': 'institute', 'f': 'field', 'v': 'venue'}

benchmarkDir = parentDir + '/benchmarks/' + dataset + '/'

entity2idReadPath = benchmarkDir + 'entity2id.txt'
f = open(entity2idReadPath, 'r')
s = f.read().split('\n')
f.close()
entityNum = int(s[0])

idIndex = dict()
typeIndex = dict()
entities = dict()
for type in types:
    entities[type] = []
for line in s:
    splited = line.split('\t')
    if len(splited) != 2:
        continue
    if len(splited[0]) != 9:
        continue
    idIndex[splited[0][1:]] = splited[1]
    idIndex[splited[1]] = splited[0][1:]
    typeIndex[splited[0][1:]] = typeMap[splited[0][0]]
    entities[typeMap[splited[0][0]]].append(splited[0][1:])

configReadPath = parentDir + '/scripts/config/' + method + '.config'
f = open(configReadPath, 'r')
s = f.read().split('\n')[order]
f.close()
dimension = int(s.split('dimension=')[1].split()[0])
pcaDimension = max(min(parsedConfig.pca, dimension), 1) if parsedConfig.pca else None

infoReadDir = parentDir + '/data/' + dataset + '/info/'
vectorReadDir = parentDir + '/res/' + '/'.join([dataset, method, str(order)]) + '/'

entityVectors = dict()
latent = dict()
coeff = []
for type in types:
    infoReadPath = infoReadDir + type + 'Info.data'
    f = open(infoReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    entityList = []
    for line in s:
        splited = line.split('\t')
        if len(splited) < 2:
            continue
        entityList.append(splited[0])

    vectorReadPath = vectorReadDir + type + 'Vector.data'
    f = open(vectorReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    for i in range(len(s)):
        splited = s[i].split('\t')
        if len(splited) != dimension:
            continue
        entityVectors[entityList[i]] = list(map(lambda x: float(x), splited))

    coeffReadPath = vectorReadDir + 'pca/' + type + 'Coeff.data'
    f = open(coeffReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    for line in s:
        splited = line.split()
        if len(splited) != dimension:
            continue
        coeff.append(list(map(lambda x: float(x), splited)))

    latentReadPath = vectorReadDir + 'pca/' + type + 'Latent.data'
    f = open(latentReadPath, 'r')
    s = f.read().split('\n')[0].split()
    f.close()
    latent[type] = list(map(lambda x: float(x), s))

relationVectors = dict()
relationReadPath = vectorReadDir + 'relationVector.data'
f = open(relationReadPath, 'r')
s = f.read().split('\n')
f.close()
for i in range(len(s)):
    splited = s[i].split('\t')
    if len(splited) != dimension:
        continue
    relationVectors[str(i)] = list(map(lambda x: float(x), splited))
relations = sorted(relationVectors.keys())

relation2idReadPath = benchmarkDir + 'relation2id.txt'
f = open(relation2idReadPath, 'r')
s = f.read().split('\n')
f.close()
relationName = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    relationName[splited[1]] = splited[0]


def triplets(head, tail, relation):
    return '\t'.join([head, tail, relation])


tripletsReadPath = benchmarkDir + 'triplets.txt'
f = open(tripletsReadPath, 'r')
s = f.read().split('\n')
f.close()
tripletsFinder = set()
for line in s:
    splited = line.split()
    if len(splited) != 3:
        continue
    tripletsFinder.add(triplets(splited[0][1:], splited[2][1:], splited[1]))


def calcDistance(v1, v2, norm):
    if len(v1) != len(v2) or len(v1) != dimension:
        raise RuntimeError('Dimension not aligned!')
    d = 0
    for i in range(dimension):
        d += abs(v1[i] - v2[i]) ** norm
    return d / dimension


def calcDistancePCA(v1, v2, type):
    if len(v1) != len(v2) or len(v1) != dimension:
        raise RuntimeError('Dimension not aligned!')
    v1PCA = [0] * dimension
    v2PCA = [0] * dimension
    for i in range(pcaDimension):
        for j in range(dimension):
            v1PCA[i] += v1[j] * coeff[j][i]
            v2PCA[i] += v2[j] * coeff[j][i]
    d = 0
    for i in range(pcaDimension):
        d += ((v1PCA[i] - v2PCA[i]) * latent[type][i]) ** 2
    return d


def updateStatistics(rank, relation, predictObject):
    global MRR, hit10, hit3, hit1
    MRR[predictObject][relation] = MRR[predictObject].get(relation, 0) + 1 / float(rank)
    hit10[predictObject][relation] = hit10[predictObject].get(relation, 0) + (1 if rank <= 10 else 0)
    hit3[predictObject][relation] = hit3[predictObject].get(relation, 0) + (1 if rank <= 3 else 0)
    hit1[predictObject][relation] = hit1[predictObject].get(relation, 0) + (1 if rank <= 1 else 0)


testReadPath = benchmarkDir + 'test2id.txt'
if testString is None:
    f = open(testReadPath, 'r')
    s = f.read().split('\n')
    f.close()
else:
    s = ['1', testString]

f = open(vectorReadDir + 'test_norm=' + str(round(norm, 2)).rstrip('.0') + '.log', 'w')
MRR = dict()
hit10 = dict()
hit3 = dict()
hit1 = dict()
for predictObject in ['head', 'tail']:
    MRR[predictObject] = dict()
    hit10[predictObject] = dict()
    hit3[predictObject] = dict()
    hit1[predictObject] = dict()
relationCount = dict()
output(f, 'Total test triplets:\t' + s[0])
testTriplets = []
for line in s:
    splited = line.split()
    if len(splited) != 3:
        continue
    testTriplets.append([splited[0], splited[1], splited[2]])

testTriplets.sort(key=lambda x: (int(x[2]), int(x[0]), int(x[1])))
for testCount in range(len(testTriplets)):
    output(f, testCount + 1, end='\t')
    head = idIndex[testTriplets[testCount][0]]
    tail = idIndex[testTriplets[testCount][1]]
    relation = testTriplets[testCount][2]
    headVector = entityVectors[head]
    tailVector = entityVectors[tail]
    relationVector = relationVectors[relation]
    headType = typeIndex[head]
    tailType = typeIndex[tail]
    relationCount[relation] = relationCount.get(relation, 0) + 1
    output(f, entityInfo(head), end='\t')
    output(f, entityInfo(tail), end='\t')

    # Predict head
    headPredictVector = [tailVector[i] - relationVector[i] for i in range(dimension)]

    distance = dict()
    for entity in entities[headType]:
        if pcaDimension is None:
            distance[entity] = calcDistance(headPredictVector, entityVectors[entity], norm)
        else:
            distance[entity] = calcDistancePCA(headPredictVector, entityVectors[entity], headType)
    sortedDistance = sorted(distance.keys(), key=lambda x: distance[x])

    rank = 1
    minIncorrectHead = '________'
    minIncorrectValueHead = -1
    findFlag = False
    for i in range(len(sortedDistance)):
        entity = sortedDistance[i]
        if superFilter:
            if not triplets(entity, tail, relation) in tripletsFinder:
                rank += 1
            else:
                break
        else:
            if entity == head:
                findFlag = True
                if minIncorrectValueHead >= 0:
                    break
            if not triplets(entity, tail, relation) in tripletsFinder:
                if minIncorrectValueHead < 0:
                    minIncorrectValueHead = distance[entity]
                    minIncorrectHead = entity
                    if findFlag:
                        break
                rank += 1
    updateStatistics(rank, relation, 'head')
    output(f, 'Head rank: ' + str(rank), end='\t')

    del headPredictVector
    del distance
    del sortedDistance

    # Predict tail
    tailPredictVector = [headVector[i] + relationVector[i] for i in range(dimension)]

    distance = dict()
    for entity in entities[tailType]:
        if pcaDimension is None:
            distance[entity] = calcDistance(tailPredictVector, entityVectors[entity], norm)
        else:
            distance[entity] = calcDistancePCA(tailPredictVector, entityVectors[entity], tailType)
    sortedDistance = sorted(distance.keys(), key=lambda x: distance[x])

    rank = 1
    minIncorrectTail = '________'
    minIncorrectValueTail = -1
    findFlag = False
    for i in range(len(sortedDistance)):
        entity = sortedDistance[i]
        if superFilter:
            if not triplets(head, entity, relation) in tripletsFinder:
                rank += 1
            else:
                break
        else:
            if entity == tail:
                findFlag = True
                if minIncorrectValueTail >= 0:
                    break
            if not triplets(head, entity, relation) in tripletsFinder:
                if minIncorrectValueTail < 0:
                    minIncorrectValueTail = distance[entity]
                    minIncorrectTail = entity
                    if findFlag:
                        break
                rank += 1
    updateStatistics(rank, relation, 'tail')
    output(f, 'Tail rank: ' + str(rank), end='\n')

    if not superFilter:
        output(f, 'Value of correct entity: ' + formattedRound(distance[tail], 4))
        output(f, 'Minimal incorrect head: ' + entityInfo(minIncorrectHead) + ' ' +
               'value: ' + formattedRound(minIncorrectValueHead, 4))
        output(f, 'Minimal incorrect tail: ' + entityInfo(minIncorrectTail) + ' ' +
               'value: ' + formattedRound(minIncorrectValueTail, 4))

    del tailPredictVector
    del distance
    del sortedDistance

    gc.collect()


def overallOutput():
    for predictObject in ['head', 'tail']:
        for relation in relations:
            MRR[predictObject][relation] /= float(relationCount[relation])
            hit10[predictObject][relation] /= float(relationCount[relation])
            hit3[predictObject][relation] /= float(relationCount[relation])
            hit1[predictObject][relation] /= float(relationCount[relation])

            MRR['overall'] = MRR.get('overall', 0) + MRR[predictObject][relation]
            hit10['overall'] = hit10.get('overall', 0) + hit10[predictObject][relation]
            hit3['overall'] = hit3.get('overall', 0) + hit3[predictObject][relation]
            hit1['overall'] = hit1.get('overall', 0) + hit1[predictObject][relation]

    MRR['overall'] /= len(relations) * 2
    hit10['overall'] /= len(relations) * 2
    hit3['overall'] /= len(relations) * 2
    hit1['overall'] /= len(relations) * 2

    output(f, 'Overall:')
    output(f, 'MRR\thit@10\thit@3\thit@1')
    output(f, '\t'.join(
        [formattedRound(MRR['overall'], 4), formattedRound(hit10['overall'], 4), formattedRound(hit3['overall'], 4),
         formattedRound(hit1['overall'], 4)]))
    output(f)

    for relation in relations:
        output(f, relationName[relation])
        output(f, '\tMRR\thit@10\thit@3\thit@1')
        for predictObject in ['head', 'tail']:
            output(f, predictObject + '\t'.join(
                ['', formattedRound(MRR[predictObject][relation], 4), formattedRound(hit10[predictObject][relation], 4),
                 formattedRound(hit3[predictObject][relation], 4), formattedRound(hit1[predictObject][relation], 4)]))
        output(f)


if testString is None:
    overallOutput()

f.close()
