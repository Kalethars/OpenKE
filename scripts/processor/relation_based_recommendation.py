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


def parseInfo(typ, infoLine):  # return entityId, entityName
    splited = infoLine.split('\t')
    if typ == 'venue':
        return splited[0].strip(), splited[2].strip() + '\t' + splited[3].strip().replace('.', ' ')
    else:
        return splited[0].strip(), splited[1].strip()


def camel(s):
    splited = s.split('_')
    return splited[0] + ''.join(list(map(lambda x: x.capitalize(), splited[1:])))


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def buildTriplet(h, r, t, reversed=False):
    if reversed:
        return ' '.join([t, r, h])
    else:
        return ' '.join([h, r, t])


def loadTriplets():
    f = open(parentDir + '/benchmarks/%s/triplets.txt' % database)
    s = f.read().split('\n')
    f.close()

    triplets = set()
    typeConstraint = [dict(), dict()]
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        headId = splited[0][1:]
        relationId = splited[1]
        tailId = splited[2][1:]
        triplets.add(buildTriplet(splited[0][1:], splited[1], splited[2][1:]))
        addToSet(typeConstraint[0], relationId, headId)
        addToSet(typeConstraint[1], relationId, tailId)

    return triplets, typeConstraint


def specialCaseValidation(relationId, recommendId, direction):
    if relationId == '3':
        if not recommendId in typeConstraint[direction][relationId]:
            return False
    return True


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

infoReadDir = parentDir + '/data/%s/info/' % database
benchmarkDir = parentDir + '/benchmarks/%s/' % database
recommendationDir = parentDir + '/res/%s/%s/%i/recommendation/' % (database, method, order)

entityName = dict()
vectors = dict()
for typ in types:
    f = codecs.open(infoReadDir + typ + 'Info.data', 'r', 'gbk')
    infoLines = f.read().split('\n')
    f.close()

    for i in range(len(infoLines) - 1):
        entityInfo = parseInfo(typ, infoLines[i])
        entityName[entityInfo[0]] = entityInfo[1].encode('utf-8').decode('ascii', 'ignore')

f = open(benchmarkDir + 'entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

entityIndex = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    entityIndex[splited[1]] = splited[0][1:]

relationMap = {'work_in': 'author_work_in_institute',
               'paper_is_written_by': 'paper_is_written_by_author',
               'paper_publish_on': 'paper_publish_on_venue',
               'paper_cit_paper': 'paper_cite_paper',
               'field_is_part_of': 'field_is_part_of_field'
               }
f = open(benchmarkDir + 'relation2id.txt', 'r')
s = f.read().split('\n')
f.close()

relationName = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    relationName[splited[1]] = camel(relationMap.get(splited[0], splited[0]))

triplets, typeConstraint = loadTriplets()

rawLogDir = recommendationDir + 'raw/'
fileList = os.listdir(rawLogDir)
for fileName in fileList:
    if 'relation=' in fileName and 'recommend=' in fileName:
        relationId = re.split('\.|_', fileName.split('relation=')[1])[0]
        recommendObject = re.split('\.|_', fileName.split('recommend=')[1])[0]
        givenObject = 'head' if recommendObject == 'tail' else 'tail'

        outputPath = recommendationDir + 'recommendation_%s_%s.txt' % (relationName[relationId], recommendObject)
        if not update and os.path.exists(outputPath):
            continue

        f = open(rawLogDir + fileName, 'r')
        s = f.read().split('\n')
        f.close()

        givenIds = []
        recommendInfos = dict()
        i = 0
        while i < len(s):
            line = s[i]
            if '%s = ' % givenObject in line and 'relation = ' in line:
                given = re.split('\.|,', line.split('%s = ' % givenObject)[1])[0]
                givenId = entityIndex[given]
                givenIds.append(givenId)
                count = int(re.split('\.|,', line.split('count = ')[1])[0])

                recommendInfos[givenId] = []
                for j in range(count):
                    recommendLine = s[i + j + 1]
                    recommendInfos[givenId].append(map(lambda x: x.strip(), recommendLine.split()))
                i = i + count + 1
            else:
                i += 1

        f = open(outputPath, 'w')
        givenIds = sorted(givenIds, key=lambda x: entityName[x])
        for givenId in givenIds:
            f.write('Recommend: %s - %s\n' % (givenId, entityName[givenId]))
            f.write('-' * 50 + '\n')
            count = 0
            for i in range(len(recommendInfos[givenId])):
                recommendInfo = recommendInfos[givenId][i]
                recommendId = entityIndex[recommendInfo[0]]
                recommendName = entityName[recommendId].encode('utf-8').decode('ascii', 'ignore')
                recommendRank = recommendInfo[1]
                recommendDist = recommendInfo[2]

                if buildTriplet(givenId, relationId, recommendId, givenObject == 'tail') in triplets:
                    continue
                if specialCaseValidation(relationId, recommendId, recommendObject == 'tail'):
                    continue
                f.write('%s\t%s\t%s\n' % (recommendRank, recommendId, recommendName))

                count += 1
                if count == 10:
                    break
            f.write('\n')
        f.close()
