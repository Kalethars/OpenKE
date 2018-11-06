# -*- coding: UTF-8 -*-

# Execution order:
# result_mapper -> pca_results_saver -> result_recommendation

import argparse
import os


def parseParams(line):
    paramMap = dict()
    splitedLine = line.split()
    for each in splitedLine:
        pos = each.find('=')
        if pos >= 0:
            paramMap[each[:pos]] = each[pos + 1:]

    return paramMap


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--dimension', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order
update = parsedArgs.update if parsedArgs.update else False

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

types = ['paper', 'author', 'institute', 'field', 'venue']

f = open(parentDir + '/benchmarks/' + database + '/entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

typeIndex = dict()
entities = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    entities[int(splited[1])] = splited[0][1:]

configReadPath = parentDir + '/scripts/config/' + method + '.config'
if os.path.exists(configReadPath):
    f = open(configReadPath, 'r')
    s = f.read().split('\n')
    f.close()
    parsedParams = parseParams(s[order])
    dimension = parsedParams['dimension']
else:
    dimension = parsedArgs.dimension
    if dimension == None:
        raise ValueError('Dimension missing!')

resultPath = parentDir + '/res/' + database + '/' + method + '/' + str(order) + '/'
f = open(resultPath + 'embedding.vec.json', 'r')
s = str(f.read())
f.close()

relationRaw = s.split('"rel_embeddings": [')[1].split(']],')[0].split('], ')
entityRaw = s.split('"ent_embeddings": [')[1].split('}')[0].split('], ')

dataSavePath = resultPath + 'relationVector.data'
if update or not os.path.exists(dataSavePath):
    f = open(dataSavePath, 'w')
    for i in range(len(relationRaw)):
        line = relationRaw[i][1:]
        splited = line.split(', ')
        if len(splited) != int(dimension):
            continue
        f.write('\t'.join(splited) + '\n')
    f.close()

vectors = dict()
for i in range(len(entityRaw)):
    line = entityRaw[i][1:]
    splited = line.split(', ')
    if len(splited) != int(dimension):
        continue
    vectors[entities[i]] = splited

for type in types:
    infoReadPath = parentDir + '/data/' + database + '/info/' + type + 'Info.data'
    if not os.path.exists(infoReadPath):
        continue

    f = open(infoReadPath, 'r')
    s = f.read().split('\n')
    f.close()

    dataSavePath = resultPath + type + 'Vector.data'
    if not update:
        if os.path.exists(dataSavePath):
            continue
    f = open(dataSavePath, 'w')
    for line in s:
        splited = line.split()
        if len(splited) <= 1:
            continue
        vector = vectors[splited[0]]
        for i in range(len(vector)):
            f.write(str(vector[i]).strip('[]'))
            f.write('\t' if i < len(vector) - 1 else '\n')
    f.close()
