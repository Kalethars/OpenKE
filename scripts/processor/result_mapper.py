# -*- coding: UTF-8 -*-

# Execution order:
# result_mapper -> pca_results_saver -> result_recommendation

import argparse
import os
import json


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

entities = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    entities[splited[0][1:]] = int(splited[1])

resultPath = parentDir + '/res/' + database + '/' + method + '/' + str(order) + '/'
f = open(resultPath + 'embedding.vec.json', 'r')
s = str(f.read())
f.close()

data = json.loads(s)

dataSavePath = resultPath + 'relationVector.data'
if update or not os.path.exists(dataSavePath):
    f = open(dataSavePath, 'w')
    for i in range(len(data['rel_embeddings'])):
        f.write('\t'.join(list(map(lambda x: str(x), data['rel_embeddings'][i]))) + '\n')
    f.close()

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
        f.write('\t'.join(list(map(lambda x: str(x), data['ent_embeddings'][entities[splited[0]]]))) + '\n')
    f.close()

if 'normal_vectors' in data.keys():
    dataSavePath = resultPath + 'normalVector.data'
    if update or not os.path.exists(dataSavePath):
        f = open(dataSavePath, 'w')
        for i in range(len(data['normal_vectors'])):
            f.write('\t'.join(list(map(lambda x: str(x), data['normal_vectors'][i]))) + '\n')
        f.close()
