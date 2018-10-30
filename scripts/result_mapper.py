# -*- coding: UTF-8 -*-

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
parser.add_argument('--database', type=str, required=True)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parsedArgs = parser.parse_args()

database = parsedArgs.database
method = parsedArgs.method
order = parsedArgs.order

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

f = open(parentDir + '/scripts/config/' + method + '.config', 'r')
s = f.read().split('\n')
f.close()
parsedParams = parseParams(s[order])

resultPath = parentDir + '/res/' + database + '/' + method + '/' + str(order) + '/'
f = open(resultPath + 'embedding.vec.json', 'r')
s = f.read().split('"ent_embeddings": [')[1].split('}')[0].split('], ')
f.close()

vectors = dict()
for i in range(len(s)):
    line = s[i][1:]
    splited = line.split(', ')
    if len(splited) != int(parsedParams['dimension']):
        continue
    vectors[entities[i]] = splited

for type in types:
    infoReadPath = parentDir + '/data/' + database + '/index/' + type + 'Index.data'
    if not os.path.exists(infoReadPath):
        continue

    f = open(infoReadPath, 'r')
    s = f.read().split('\n')
    f.close()

    dataSavePath = resultPath + type + 'Data.data'
    f = open(dataSavePath, 'w')
    for line in s:
        splited = line.split()
        if len(splited) <= 1:
            continue
        vector = vectors[splited[0]]
        for i in range(len(vector)):
            f.write(str(vector[i]))
            f.write('\t' if i < len(vector) - 1 else '\n')
    f.close()
