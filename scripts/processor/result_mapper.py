# -*- coding: UTF-8 -*-

# Execution order:
# result_mapper -> pca_results_saver -> result_recommendation

import argparse
import codecs
import json
import os

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
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--update', type=bool, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
update = parsedArgs.update if parsedArgs.update else False

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
    if not 'ComplEx' in method:
        for i in range(len(data['rel_embeddings'])):
            f.write('\t'.join(list(map(lambda x: str(x), data['rel_embeddings'][i]))) + '\n')
    else:
        for i in range(len(data['rel_re_embeddings'])):
            vector = [complex(data['rel_re_embeddings'][i][j], data['ent_im_embeddings'][i][j])
                      for j in range(len(data['rel_re_embeddings'][i]))]
            f.write('\t'.join(list(map(lambda x: str(x), vector))) + '\n')
    f.close()

for type in types:
    infoReadPath = parentDir + '/data/' + database + '/info/' + type + 'Info.data'
    if not os.path.exists(infoReadPath):
        continue

    f = codecs.open(infoReadPath, 'r', 'gbk')
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
        entityId = entities[splited[0]]
        if not 'ComplEx' in method:
            vector = data['ent_embeddings'][entityId]
            if 'TransH' in method or 'DistMult' in method:
                l2norm = sum([abs(vector[i]) ** 2 for i in range(len(vector))]) ** 0.5
                vector = [vector[i] / l2norm for i in range(len(vector))]
            f.write('\t'.join(list(map(lambda x: str(x), vector))) + '\n')
        else:
            vector = [complex(data['ent_re_embeddings'][entityId][i], data['ent_im_embeddings'][entityId][i])
                      for i in range(len(data['ent_re_embeddings'][entityId]))]
            l2norm = sum([abs(vector[i]) ** 2 for i in range(len(vector))]) ** 0.5
            vector = [vector[i] / l2norm for i in range(len(vector))]
            f.write('\t'.join(list(map(lambda x: str(x), vector))) + '\n')
    f.close()

if 'normal_vectors' in data.keys():
    dataSavePath = resultPath + 'normalVector.data'
    if update or not os.path.exists(dataSavePath):
        f = open(dataSavePath, 'w')
        for i in range(len(data['normal_vectors'])):
            f.write('\t'.join(list(map(lambda x: str(x), data['normal_vectors'][i]))) + '\n')
        f.close()
