import tensorflow as tf
import numpy as np
import argparse
import os

# result_mapper -> transe_test_tensorflow

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--superfilter', type=bool, required=False)
parser.add_argument('--norm', type=float, required=False)
parsedConfig = parser.parse_args()

dataset = parsedConfig.dataset if parsedConfig.dataset else 'ACE17K'
method = parsedConfig.method if parsedConfig.method else 'TransE'
order = parsedConfig.order
superFilter = parsedConfig.superfilter if parsedConfig.superfilter else False
norm = parsedConfig.norm if parsedConfig.norm else 1

types = ['paper', 'author', 'institute', 'field', 'venue']
typeMap = {'p': 'paper', 'a': 'author', 'i': 'institute', 'f': 'field', 'v': 'venue'}

benchmarkDir = parentDir + '/benchmarks/' + dataset + '/'

entity2idReadPath = benchmarkDir + 'entity2id.txt'
f = open(entity2idReadPath, 'r')
s = f.read().split('\n')
f.close()
idIndex = dict()
typeIndex = dict()
entities = dict()
entityLocation = dict()
for typ in types:
    entities[typ] = []
entityNum = int(s[0])
for line in s:
    splited = line.split('\t')
    if len(splited) != 2:
        continue
    if len(splited[0]) != 9:
        continue
    dbId = splited[0][1:]
    typeAbbr = splited[0][0]
    numId = int(splited[1])
    idIndex[dbId] = numId
    idIndex[numId] = dbId
    typeIndex[numId] = typeMap[typeAbbr]
    entityLocation[numId] = len(entities[typeMap[typeAbbr]])
    entities[typeMap[typeAbbr]].append(numId)

configReadPath = parentDir + '/scripts/config/' + method + '.config'
f = open(configReadPath, 'r')
s = f.read().split('\n')[order]
f.close()
dimension = int(s.split('dimension=')[1].split()[0])

infoReadDir = parentDir + '/data/' + dataset + '/info/'
vectorReadDir = parentDir + '/res/' + '/'.join([dataset, method, str(order)]) + '/'

entityVectors = [[] for i in range(entityNum)]
latent = [[] for i in range(len(types))]
coeff = [[] for i in range(len(types))]
for n in range(len(types)):
    typ = types[n]
    infoReadPath = infoReadDir + typ + 'Info.data'
    f = open(infoReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    entityList = []
    for line in s:
        splited = line.split('\t')
        if len(splited) < 2:
            continue
        entityList.append(idIndex[splited[0]])

    vectorReadPath = vectorReadDir + typ + 'Vector.data'
    f = open(vectorReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    for i in range(len(s)):
        splited = s[i].split('\t')
        if len(splited) != dimension:
            continue
        entityVectors[entityList[i]] = list(map(lambda x: float(x), splited))

    coeffReadPath = vectorReadDir + 'pca/' + typ + 'Coeff.data'
    f = open(coeffReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    for line in s:
        splited = line.split()
        if len(splited) != dimension:
            continue
        coeff[n].append(list(map(lambda x: float(x), splited)))

    latentReadPath = vectorReadDir + 'pca/' + typ + 'Latent.data'
    f = open(latentReadPath, 'r')
    s = f.read().split('\n')[0].split()
    f.close()
    latent[n] = list(map(lambda x: float(x), s))

for i in range(len(entityVectors)):
    if len(entityVectors[i]) != dimension:
        entityVectors[i] = [0] * dimension

relationReadPath = vectorReadDir + 'relationVector.data'
f = open(relationReadPath, 'r')
s = f.read().split('\n')
f.close()
relationVectors = []
for i in range(len(s)):
    splited = s[i].split('\t')
    if len(splited) != dimension:
        continue
    relationVectors.append(list(map(lambda x: float(x), splited)))
relationNum = len(relationVectors)

relation2idReadPath = benchmarkDir + 'relation2id.txt'
f = open(relation2idReadPath, 'r')
s = f.read().split('\n')
f.close()
relationName = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    relationName[int(splited[1])] = splited[0]


def triplets(head, tail, relation):
    return '\t'.join([str(head), str(tail), str(relation)])


tripletsReadPath = benchmarkDir + 'triplets.txt'
f = open(tripletsReadPath, 'r')
s = f.read().split('\n')
f.close()
tripletsFinder = set()
for line in s:
    splited = line.split()
    if len(splited) != 3:
        continue
    tripletsFinder.add(triplets(idIndex[splited[0][1:]], idIndex[splited[2][1:]], splited[1]))

# Now we have lists: entityVectors, latent, coeff, relationVectors
sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

tfEntityVectors = tf.convert_to_tensor(entityVectors)
tfLatent = tf.convert_to_tensor(latent)
tfCoeff = tf.convert_to_tensor(coeff)
tfRelationVectors = tf.convert_to_tensor(relationVectors)


def calcDistance(h, r, t):
    return tf.norm(h + r - t, norm, axis=1)


def updateStatistics(rank, relation, predictObject):
    global MRR, hit10, hit3, hit1
    MRR[predictObject][relation] = MRR[predictObject].get(relation, 0) + 1 / float(rank)
    hit10[predictObject][relation] = hit10[predictObject].get(relation, 0) + (1 if rank <= 10 else 0)
    hit3[predictObject][relation] = hit3[predictObject].get(relation, 0) + (1 if rank <= 3 else 0)
    hit1[predictObject][relation] = hit1[predictObject].get(relation, 0) + (1 if rank <= 1 else 0)


def output(f, s='', end='\n'):
    print(str(s) + end, end='')
    f.write(str(s) + end)


testReadPath = benchmarkDir + 'test2id.txt'
f = open(testReadPath, 'r')
s = f.read().split('\n')
f.close()
MRR = dict()
hit10 = dict()
hit3 = dict()
hit1 = dict()
for predictObject in ['head', 'tail']:
    MRR[predictObject] = dict()
    hit10[predictObject] = dict()
    hit3[predictObject] = dict()
    hit1[predictObject] = dict()
relationCount = [0] * relationNum
testCount = 0
f = open(vectorReadDir + 'test_norm=' + str(round(norm, 2)).rstrip('.0') + '.log', 'w')
output(f, 'Total test triplets:\t' + s[0])
for line in s:
    splited = line.split()
    if len(splited) != 3:
        continue
    testCount += 1
    output(f, testCount, end='\t')
    head = int(splited[0])
    tail = int(splited[1])
    relation = int(splited[2])
    headVector = tf.nn.embedding_lookup(tfEntityVectors, head)
    tailVector = tf.nn.embedding_lookup(tfEntityVectors, tail)
    relationVector = tf.nn.embedding_lookup(tfRelationVectors, relation)
    headType = typeIndex[head]
    tailType = typeIndex[tail]
    relationCount[relation] += 1
    output(f, headType[0] + idIndex[head], end='\t')
    output(f, tailType[0] + idIndex[tail], end='\t')

    # Predict head
    testTripletsNum = len(entities[headType])

    testHeads = tf.nn.embedding_lookup(tfEntityVectors, entities[headType])
    testTails = tf.nn.embedding_lookup(tfEntityVectors, [tail] * testTripletsNum)
    testRelations = tf.nn.embedding_lookup(tfRelationVectors, [relation] * testTripletsNum)

    testResults = calcDistance(testHeads, testRelations, testTails).eval()
    sortedDistance = sorted(entities[headType], key=lambda x: testResults[entityLocation[x]])

    rank = 1
    for i in range(testTripletsNum):
        entity = sortedDistance[i]
        if superFilter:
            if not triplets(entity, tail, relation) in tripletsFinder:
                rank += 1
            else:
                break
        else:
            if entity == head:
                break
            if not triplets(entity, tail, relation) in tripletsFinder:
                rank += 1
    updateStatistics(rank, relation, 'head')
    output(f, 'Head rank: ' + str(rank), end='\t')

    # Predict tail
    testTripletsNum = len(entities[tailType])

    testHeads = tf.nn.embedding_lookup(tfEntityVectors, [head] * testTripletsNum)
    testTails = tf.nn.embedding_lookup(tfEntityVectors, entities[tailType])
    testRelations = tf.nn.embedding_lookup(tfRelationVectors, [relation] * testTripletsNum)

    testResults = calcDistance(testHeads, testRelations, testTails).eval()
    sortedDistance = sorted(entities[tailType], key=lambda x: testResults[entityLocation[x]])

    rank = 1
    for i in range(testTripletsNum):
        entity = sortedDistance[i]
        if superFilter:
            if not triplets(head, entity, relation) in tripletsFinder:
                rank += 1
            else:
                break
        else:
            if entity == tail:
                break
            if not triplets(head, entity, relation) in tripletsFinder:
                rank += 1
    updateStatistics(rank, relation, 'tail')
    output(f, 'Tail rank: ' + str(rank))

for predictObject in ['head', 'tail']:
    for relation in range(relationNum):
        MRR[predictObject][relation] /= float(relationCount[relation])
        hit10[predictObject][relation] /= float(relationCount[relation])
        hit3[predictObject][relation] /= float(relationCount[relation])
        hit1[predictObject][relation] /= float(relationCount[relation])

        MRR['overall'] = MRR.get('overall', 0) + MRR[predictObject][relation]
        hit10['overall'] = hit10.get('overall', 0) + hit10[predictObject][relation]
        hit3['overall'] = hit3.get('overall', 0) + hit3[predictObject][relation]
        hit1['overall'] = hit1.get('overall', 0) + hit1[predictObject][relation]

MRR['overall'] /= relationNum * 2
hit10['overall'] /= relationNum * 2
hit3['overall'] /= relationNum * 2
hit1['overall'] /= relationNum * 2


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


output(f, 'Overall:')
output(f, '\tMRR\thit@10\thit@3\thit@1')
output(f, '\t'.join(
    [formattedRound(MRR['overall'], 4), formattedRound(hit10['overall'], 4), formattedRound(hit3['overall'], 4),
     formattedRound(hit1['overall'], 4)]))
output(f)

for relation in range(relationNum):
    output(f, relationName[relation])
    output(f, '\t\tMRR\thit@10\thit@3\thit@1')
    for predictObject in ['head', 'tail']:
        output(f, predictObject + '\t'.join(
            ['', formattedRound(MRR[predictObject][relation], 4), formattedRound(hit10[predictObject][relation], 4),
             formattedRound(hit3[predictObject][relation], 4), formattedRound(hit1[predictObject][relation], 4)]))
    output(f)

f.close()
