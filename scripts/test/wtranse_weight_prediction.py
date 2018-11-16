import argparse
import os

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def entityInfo(entity):
    return typeIndex.get(entity, '_')[0] + entity + \
           '(' + str(idIndex[entity]) + ')' + ' ' * (len(str(entityNum)) - len(str(idIndex[entity])))


def output(f, s='', end='\n'):
    print(str(s) + end, end='')
    f.write(str(s) + end)


parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--norm', type=float, required=False)
parser.add_argument('--dimension', type=int, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method if parsedConfig.method else 'WTransE'
order = parsedConfig.order
norm = parsedConfig.norm if parsedConfig.norm else 1

types = ['paper', 'author', 'institute', 'field', 'venue']
typeMap = {'p': 'paper', 'a': 'author', 'i': 'institute', 'f': 'field', 'v': 'venue'}

benchmarkDir = parentDir + '/benchmarks/' + database + '/'

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

try:
    configReadPath = parentDir + '/scripts/config/' + method + '.config'
    f = open(configReadPath, 'r')
    s = f.read().split('\n')[order]
    f.close()
    dimension = int(s.split('dimension=')[1].split()[0])
except:
    dimension = parsedConfig.dimension

infoReadDir = parentDir + '/data/' + database + '/info/'
vectorReadDir = parentDir + '/res/' + '/'.join([database, method, str(order)]) + '/'

entityVectors = dict()
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

tripletsReadPath = benchmarkDir + 'triplets_weight.txt'
f = open(tripletsReadPath, 'r')
s = f.read().split('\n')
f.close()
maxWeight = -1
minWeight = 10000
for line in s:
    splited = line.split()
    if len(splited) != 4:
        continue
    maxWeight = max(maxWeight, float(splited[3]))
    minWeight = min(minWeight, float(splited[3]))


def constMultiply(v, c):
    return [v[i] * c for i in range(len(v))]


def calcDistance(v1, v2, norm):
    if len(v1) != len(v2) or len(v1) != dimension:
        raise RuntimeError('Dimension not aligned!')
    d = 0
    for i in range(dimension):
        d += abs(v1[i] - v2[i]) ** norm
    return d


testReadPath = benchmarkDir + 'test2id_weighted.txt'
f = open(testReadPath, 'r')
s = f.read().split('\n')
f.close()

f = open(vectorReadDir + 'weight_prediction.log', 'w')
output(f, 'Min weight: %s\tMax weight:%s\t' % (formattedRound(minWeight, 4), formattedRound(maxWeight, 4)))
output(f, 'Total test triplets:\t' + s[0])
testTriplets = []
for line in s:
    splited = line.split()
    if len(splited) != 4:
        continue
    testTriplets.append([splited[0], splited[1], splited[2], splited[3]])

testTriplets.sort(key=lambda x: (int(x[2]), int(x[0]), int(x[1])))
for testCount in range(len(testTriplets)):
    output(f, testCount + 1, end='\t')
    head = idIndex[testTriplets[testCount][0]]
    tail = idIndex[testTriplets[testCount][1]]
    relation = testTriplets[testCount][2]
    weight = float(testTriplets[testCount][3])
    headVector = entityVectors[head]
    tailVector = entityVectors[tail]
    relationVector = relationVectors[relation]
    headType = typeIndex[head]
    tailType = typeIndex[tail]
    output(f, entityInfo(head), end='\t')
    output(f, entityInfo(tail), end='\t')

    difference = [tailVector[i] - headVector[i] for i in range(dimension)]
    standardDistance = calcDistance(difference, constMultiply(relationVector, 1 / weight), norm)

    bestDistance = -1
    for testWeight in [minWeight, maxWeight]:
        weightedRelation = constMultiply(relationVector, 1 / testWeight)
        distance = calcDistance(difference, weightedRelation, norm)
        if distance < bestDistance or bestDistance < 0:
            bestDistance = distance
            predictWeight = testWeight
    for i in range(dimension):
        if relationVector[i] == 0 or difference[i] == 0:
            continue
        coefficient = difference[i] / relationVector[i]
        if 1 / coefficient < minWeight or 1 / coefficient > maxWeight:
            continue
        weightedRelation = constMultiply(relationVector, coefficient)
        distance = calcDistance(difference, weightedRelation, norm)
        if distance < bestDistance:
            bestDistance = distance
            predictWeight = 1 / coefficient

    output(f, 'Weight: ' + formattedRound(weight, 4), end='\t')
    output(f, 'Predict: ' + formattedRound(predictWeight, 4), end='\t')

    output(f, 'Distance: ' + formattedRound(standardDistance, 4), end='\t')
    output(f, 'Predict: ' + formattedRound(bestDistance, 4), end='\n')

f.close()
