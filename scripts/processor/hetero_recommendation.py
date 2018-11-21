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

entityName = dict()
vectors = dict()
for typ in types:
    f = codecs.open(infoReadDir + typ + 'Info.data', 'r', 'gbk')
    infoLines = f.read().split('\n')
    f.close()

    for i in range(len(infoLines) - 1):
        entityInfo = parseInfo(typ, infoLines[i])
        entityName[entityInfo[0]] = entityInfo[1]

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

fileList = os.listdir(recommendationDir)
for fileName in fileList:
    if 'relation=' in fileName and 'recommend=' in fileName:
        relationId = re.split('\.|_', fileName.split('relation=')[1])[0]
        recommendObject = re.split('\.|_', fileName.split('recommend=')[1])[0]
        givenObject = 'head' if recommendObject == 'tail' else 'tail'

        f = open(recommendationDir + fileName, 'r')
        s = f.read().split('\n')
        f.close()

        givenIds = []
        recommendIds = dict()
        for i in range(len(s)):
            line = s[i]
            if '%s = ' % givenObject in line and 'relation = ' in line:
                given = re.split('\.|,', line.split('%s = ' % givenObject)[1])[0]
                givenId = entityIndex[given]
                givenIds.append(givenId)

                recommendLine = s[i + 1]
                recommendIds[givenId] = list(map(lambda x: x.strip(), recommendLine.split()))

        f = open(recommendationDir + 'analyzed/recommendation_%s_%s.txt' %
                 (relationName[relationId], recommendObject), 'w')
        givenIds = sorted(givenIds, key=lambda x: entityName[x])
        for givenId in givenIds:
            f.write('Recommend: %s - %s\n' % (givenId, entityName[givenId]))
            f.write('-' * 50 + '\n')
            for i in range(0, len(recommendIds[givenId]), 2):
                recommendId = entityIndex[recommendIds[givenId][i]]
                recommendName = entityName[recommendId]
                recommendRank = recommendIds[givenId][i + 1]
                f.write('%s\t%s\t%s\n' % (recommendRank, recommendId, relationName))
            f.write('\n')
        f.close()
