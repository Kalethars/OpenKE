import argparse
import re
import os
import codecs

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

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


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def getId(infoLine):  # return entityId
    return infoLine.split('\t')[0].strip()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)

types = ['paper', 'author', 'institute', 'field', 'venue']

infoReadDir = parentDir + '/data/%s/info/' % database
benchmarkDir = parentDir + '/benchmarks/%s/' % database
recommendationDir = parentDir + '/res/%s/%s/%i/recommendation/' % (database, method, order)

f = open(benchmarkDir + 'entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

entityIndex = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    entityIndex[splited[1]] = splited[0][1:]
    entityIndex[splited[0][1:]] = splited[1]

entityList = dict()
availableSet = dict()
vectors = dict()
for typ in types:
    f = codecs.open(infoReadDir + typ + 'Info.data', 'r', 'gbk')
    infoLines = f.read().split('\n')
    f.close()

    entityList[typ] = []
    for i in range(len(infoLines) - 1):
        entityId = getId(infoLines[i])
        entityList[typ].append(entityId)
    availableSet[typ] = set(entityList[typ])

mkdir(['res', database, method, order, 'distmap'])
distmapDir = parentDir + '/res/%s/%s/%i/distmap/' % (database, method, order)

relationHeadType = ['author', 'author', 'paper', 'paper', 'paper', 'paper', 'field']
relationTailType = ['institute', 'field', 'author', 'field', 'venue', 'paper', 'field']

rawLogDir = recommendationDir + 'raw/'
fileList = os.listdir(rawLogDir)
for fileName in fileList:
    if 'relation=' in fileName and 'recommend=' in fileName:
        relationId = int(re.split('\.|_', fileName.split('relation=')[1])[0])
        recommendObject = re.split('\.|_', fileName.split('recommend=')[1])[0]
        givenObject = 'head' if recommendObject == 'tail' else 'tail'
        direction = 'pos' if givenObject == 'head' else 'neg'

        print('Mapping distance of relation %i by %s' % (relationId, direction))

        givenType = relationHeadType[relationId] if givenObject == 'head' else relationTailType[relationId]
        recommendType = relationTailType[relationId] if givenObject == 'head' else relationHeadType[relationId]

        f = open(rawLogDir + fileName, 'r')
        s = f.read().split('\n')
        f.close()

        givenIds = []
        distances = dict()
        i = 0
        while i < len(s):
            line = s[i]
            if '%s = ' % givenObject in line and 'relation = ' in line:
                # caseId = line.split('Case ')[1].split('.')[0]
                # print('Found case: %s' % caseId)

                given = re.split('\.|,', line.split('%s = ' % givenObject)[1])[0]
                givenId = entityIndex[given]
                count = int(re.split('\.|,', line.split('count = ')[1])[0])
                if not givenId in availableSet[givenType]:
                    i += count + 1
                    continue

                distances[givenId] = dict()
                for j in range(count):
                    recommendLine = s[i + j + 1]
                    splited = recommendLine.split()
                    recommendId = entityIndex[splited[0]].strip()
                    if not recommendId in availableSet[recommendType]:
                        continue
                    distance = splited[2].strip()
                    distances[givenId][recommendId] = distance

                assert len(distances[givenId].keys()) == len(entityList[recommendType])
                i += count + 1
            else:
                i += 1

        print('Keys in distances dict: %i' % len(distances.keys()))
        print('Entities of given type: %i' % len(entityList[givenType]))
        assert len(distances.keys()) == len(entityList[givenType])

        f = open(distmapDir + 'distmap_%i_%s.data' % (relationId, direction), 'w')
        # First line for given entityIds (rows)
        for i in range(len(entityList[givenType])):
            if i == 0:
                f.write(entityList[givenType][i])
            else:
                f.write(' %s' % entityList[givenType][i])
        f.write('\n')
        # Second line for recommend entityIds (columns)
        for i in range(len(entityList[recommendType])):
            if i == 0:
                f.write(entityList[recommendType][i])
            else:
                f.write(' %s' % entityList[recommendType][i])
        f.write('\n')

        for i in range(len(entityList[givenType])):
            givenId = entityList[givenType][i]
            for j in range(len(entityList[recommendType])):
                recommendId = entityList[recommendType][j]
                if j == 0:
                    f.write(distances[givenId][recommendId])
                else:
                    f.write(' %s' % distances[givenId][recommendId])
            f.write('\n')

        f.close()
