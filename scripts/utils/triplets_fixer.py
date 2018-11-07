import argparse
import os

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parsedArgs = parser.parse_args()
database = parsedArgs.database if parsedArgs.database else 'ACE17K'
databaseDir = parentDir + '/benchmarks/' + database + '/'

f = open(databaseDir + 'entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

entityIndex = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    entityIndex[splited[1]] = splited[0]

triplets = []
for filename in ['train', 'valid', 'test']:
    f = open(databaseDir + filename + '2id.txt', 'r')
    s = f.read().split('\n')
    f.close()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        triplets.append(' '.join([entityIndex[splited[0]], splited[2], entityIndex[splited[1]]]))

f = open(databaseDir + 'triplets.txt', 'w')
for triplet in triplets:
    f.write(triplet + '\n')
f.close()
