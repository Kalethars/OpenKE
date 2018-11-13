database = 'ACE17K'

databaseDir = '../../benchmarks/%s/' % database
f = open(databaseDir + 'relation2id.txt', 'r')
s = f.read().split('\n')
f.close()
relationName = dict()
for line in s:
    splited = line.split()
    if len(splited) == 2:
        relationName[splited[1]] = splited[0]

relationCount = dict()
for filename in ['triplets', 'train2id', 'valid2id', 'test2id']:
    pos = 1 if filename == 'triplets' else 2

    f = open(databaseDir + filename + '.txt', 'r')
    s = f.read().split('\n')
    f.close()

    overall = 0
    relationCount = dict()
    for line in s:
        splited = line.split()
        if len(splited) == 3:
            relationCount[splited[pos]] = relationCount.get(splited[pos], 0) + 1
            overall += 1

    print(filename, overall)
    for relationId in ['2', '3', '4', '5', '0', '1', '6']:
        print(relationName[relationId], relationCount[relationId])
    print()
