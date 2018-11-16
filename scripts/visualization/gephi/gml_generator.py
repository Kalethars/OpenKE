import argparse
import os

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'

databaseDir = parentDir + '/benchmarks/%s/' % database
f = open(databaseDir + 'entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

entityMap = dict()
for line in s:
    splited = line.split()
    if len(splited) == 2:
        entityMap[splited[1]] = splited[0]

f = open(databaseDir + 'relation2id.txt', 'r')
s = f.read().split('\n')
f.close()

triplets = dict()
for line in s:
    splited = line.split()
    if len(splited) == 2:
        triplets[splited[1]] = []

typeMap = {'p': 'Paper', 'a': 'Author', 'i': 'Institute', 'f': 'Field', 'v': 'Venue'}
dataInfoDir = parentDir + '/data/%s/info/' % database
entityLabel = dict()
for typ in typeMap.values():
    dataInfoPath = dataInfoDir + typ.lower() + 'Info.data'
    f = open(dataInfoPath, 'r')
    s = f.read().split('\n')
    f.close()

    for line in s:
        splited = line.split('\t')
        if len(splited) >= 2:
            entityLabel[splited[0]] = splited[2 if typ == 'Venue' else 1]

f = open(databaseDir + 'triplets_weight.txt', 'r')
s = f.read().split('\n')
f.close()

entities = dict()
for typ in typeMap.values():
    entities[typ] = set()
for line in s:
    splited = line.split()
    if len(splited) == 4:
        triplets[splited[0]].append((splited[1], splited[2], splited[3]))
        entities[typeMap[entityMap[splited[1]][0]]].add(splited[1])
        entities[typeMap[entityMap[splited[2]][0]]].add(splited[2])

f = open(databaseDir + 'triplets.gml', 'w')
f.write('graph [\n')
f.write('undirected 0\n')
for typ in sorted(entities.keys()):
    for node in entities[typ]:
        id = entityMap[node]
        label = entityLabel[id[1:]]
        weight = 0
        f.write('node [\n')
        f.write('id "%s"\n' % id)
        f.write('label "%s"\n' % (label if typ in ['Field', 'Venue'] else id))
        f.write('weight %i\n' % weight)
        f.write('type "%s"\n' % typ)
        f.write(']\n')
for typ in sorted(triplets.keys()):
    for edge in triplets[typ]:
        source = entityMap[edge[0]]
        target = entityMap[edge[1]]
        weight = edge[2]
        f.write('edge [\n')
        f.write('source "%s"\n' % source)
        f.write('target "%s"\n' % target)
        f.write('weight %s\n' % weight)
        f.write('type "Directed"\n')
        f.write(']\n')
f.write(']\n')
f.close()
