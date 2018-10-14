import os

import pymysql
import math

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def connectSQL():
    global config
    conn = pymysql.connect(host=config['host'], port=int(config['port']), user=config['user'], passwd=config['passwd'],
                           db=config['db'])
    return conn


def disconnectSQL(conn):
    conn.commit()
    conn.close()


def loadConfig():
    global config
    f = open(parentDir + '/scripts/database.config')
    s = f.read().split('\n')
    f.close()
    config = dict()
    for line in s:
        splited = line.split('=')
        if len(splited) == 2:
            config[splited[0]] = splited[1]


def loadEntities():
    global entities
    entityMap = {'a': 0, 'f': 1, 'i': 2, 'p': 3, 'v': 4}
    f = open(parentDir + '/benchmarks/ACE17K/entity2id.txt', 'r')
    s = f.read().split('\n')
    f.close()
    entities = [[] for i in range(5)]
    for line in s:
        splited = line.split()
        if len(splited) == 2:
            entities[entityMap[splited[0][0]]].append(splited[0])


def loadTriplets():
    # triplets[relation] = list of [head, tail]

    global triplets
    f = open(parentDir + '/benchmarks/ACE17K/triplets_sort_relation.txt', 'r')
    s = f.read().split('\n')
    f.close()
    triplets = [[] for i in range(7)]
    for line in s:
        splited = line.split()
        if len(splited) == 3:
            triplets[int(splited[0])].append([splited[1], splited[2]])


def getDataPath(filename):
    return parentDir + '/data/ACE17K/' + filename


def loadData(filename):
    fullPath = getDataPath(filename)
    if os.path.exists(fullPath):
        return parseData(fullPath)
    else:
        return None


def parseData(fullPath):
    f = open(fullPath, 'r')
    s = f.read().split('\n')
    f.close()
    data = []
    for line in s:
        if len(line.split()) > 0:
            data.append(line.split())
    return data


def buildWeightString(relation, head, tail, weight):
    return ' '.join([str(relation), head, tail, str(weight)]) + '\n'


def downloadData():
    # For work_in, paper_is_written_by
    def paperAuthorAffiliations():
        filename = 'PaperAuthorAffiliations.data'
        if os.path.exists(getDataPath(filename)):
            return

        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for triplet in triplets[2]:  # paper_is_written_by
            query = 'select PaperId, AuthorId, AffiliationId, AuthorSequenceNumber from PaperAuthorAffiliations \
                             where PaperId="%(head)s" and AuthorId="%(tail)s"' \
                    % {'head': triplet[0][1:], 'tail': triplet[1][1:]}
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                f.write('\t'.join(map(lambda x: str(x), result)) + '\n')
        disconnectSQL(conn)

        f.close()

    # For paper_publish_on, paper_cit_paper
    def paperYears():
        filename = 'PaperYears.data'
        if os.path.exists(getDataPath(filename)):
            return

        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for paper in entities[3]:
            query = 'select PaperId, PaperPublishYear from PaperYears where PaperId="%(paper)s"' % {'paper': paper[1:]}
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                f.write('\t'.join(map(lambda x: str(x), result)) + '\n')
        disconnectSQL(conn)

        f.close()

    # For field_is_part_of_field
    def fieldOfStudyHierarchy():
        filename = 'FieldOfStudyHierarchy.data'
        if os.path.exists(getDataPath(filename)):
            return

        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for triplet in triplets[6]:  # field_is_in_field
            query = 'select ChildFieldOfStudyID, ParentFieldOfStudyID, Confidence from FieldOfStudyHierarchy \
                     where ChildFieldOfStudyID="%(head)s" and ParentFieldOfStudyID="%(tail)s"' \
                    % {'head': triplet[0][1:], 'tail': triplet[1][1:]}
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                f.write('\t'.join(map(lambda x: str(x), result)) + '\n')
        disconnectSQL(conn)

        f.close()

    paperAuthorAffiliations()
    paperYears()
    fieldOfStudyHierarchy()


def workIn():
    # relation = 0, head = author, tail = institute
    def calcWeight(triplet):
        return detailedCount.get(triplet[0][1:], dict()).get(triplet[1][1:], 0) / \
               float(totalCount.get(triplet[0][1:], 1))

    filename = 'PaperAuthorAffiliations.data'
    data = loadData(filename)

    totalCount = dict()  # Total number of papers published by an author
    detailedCount = dict()  # Number of papers published by an author from an institute
    for line in data:
        totalCount[line[1]] = totalCount.get(line[1], 0) + 1
        if detailedCount.get(line[1], 0) == 0:
            detailedCount[line[1]] = dict()
        detailedCount[line[1]][line[2]] = detailedCount[line[1]].get(line[2], 0) + 1
    f = open(weightPath, 'a')
    for triplet in triplets[0]:
        f.write(buildWeightString(0, triplet[0], triplet[1], calcWeight(triplet)))
    f.close()


def authorIsInField():
    # relation = 1, head = author, tail = field
    def calcWeight(triplet):
        return detailedCount.get(triplet[0], dict()).get(triplet[1], 0) / float(totalCount.get(triplet[0], 1))

    totalCount = dict()  # Total number of papers published by an author
    detailedCount = dict()  # Number of papers published by an author in a field
    paperAuthor = dict()
    for triplet in triplets[2]:  # paper_is_written_by
        try:
            paperAuthor[triplet[0]].append(triplet[1])
        except:
            paperAuthor[triplet[0]] = [triplet[1]]
        totalCount[triplet[1]] = totalCount.get(triplet[1], 0) + 1
    for triplet in triplets[3]:  # paper_is_in_field
        for author in paperAuthor.get(triplet[0], []):
            if detailedCount.get(author, 0) == 0:
                detailedCount[author] = dict()
            detailedCount[author][triplet[1]] = detailedCount[author].get(triplet[1], 0) + 1
    f = open(weightPath, 'a')
    for triplet in triplets[1]:
        f.write(buildWeightString(1, triplet[0], triplet[1], calcWeight(triplet)))
    f.close()


def paperIsWrittenBy():
    # relaation = 2, head = paper, tail = author
    def calcWeight(seqNum):
        return 1.0 / min(float(seqNum), 10.0)

    filename = 'PaperAuthorAffiliations.data'
    data = loadData(filename)
    f = open(weightPath, 'a')
    for line in data:
        f.write(buildWeightString(2, 'p' + line[0], 'a' + line[1], calcWeight(line[3])))
    f.close()


def paperIsInField():
    # relation = 3, head = paper, tail = field
    f = open(weightPath, 'a')
    for triplet in triplets[3]:
        f.write(buildWeightString(3, triplet[0], triplet[1], 1.0))
    f.close()


def paperPublishOn():
    # relation = 4, head = paper, tail = venue
    def calcWeight(paper):
        return max(1 - 0.04 * (lastYear - paperYears.get(paper, 0)), 0.2)

    filename = 'PaperYears.data'
    data = loadData(filename)
    paperYears = dict()
    lastYear = 0
    for line in data:
        paperYears['p' + line[0]] = int(line[1])
        if int(line[1]) > lastYear:
            lastYear = int(line[1])
    f = open(weightPath, 'a')
    for triplet in triplets[4]:
        f.write(buildWeightString(4, triplet[0], triplet[1], calcWeight(triplet[0])))
    f.close()


def paperCitPaper():
    # relation =5, head = paper, tail = paper
    def calcWeight(triplet):
        return max(1 - 0.04 * abs(paperYears.get(triplet[0], 1000) - paperYears.get(triplet[1], 0)), 0.2)

    filename = 'PaperYears.data'
    data = loadData(filename)
    paperYears = dict()
    for line in data:
        paperYears['p' + line[0]] = int(line[1])
    f = open(weightPath, 'a')
    for triplet in triplets[5]:
        f.write(buildWeightString(5, triplet[0], triplet[1], calcWeight(triplet)))
    f.close()


def fieldIsPartOfField():
    # relation = 6, head = field, tail = field
    filename = 'FieldOfStudyHierarchy.data'
    data = loadData(filename)
    f = open(weightPath, 'a')
    for line in data:
        f.write(buildWeightString(6, 'f' + line[0], 'f' + line[1], float(line[2])))
    f.close()


def normalization():
    # make average weight of each relation to 1
    def calcWeight(line):
        return round(float(line[3]) * tripletCount[line[0]] / weightSum[line[0]], 2)

    data = parseData(parentDir + '/benchmarks/ACE17K/triplets_weight.txt')
    weightSum = dict()
    tripletCount = dict()
    for line in data:
        weightSum[line[0]] = weightSum.get(line[0], 0) + float(line[3])
        tripletCount[line[0]] = tripletCount.get(line[0], 0) + 1
    f = open(weightPath, 'w')
    for line in data:
        f.write(buildWeightString(line[0], line[1], line[2], calcWeight(line)))
    f.close()


config = dict()
loadConfig()
entities = [[] for i in range(5)]  # 0 for author, 1 for field, 2 for institute, 3 for paper, 4 for venue
loadEntities()
triplets = [[] for i in range(7)]
loadTriplets()

weightPath = parentDir + '/benchmarks/ACE17K/triplets_weight.txt'
f = open(weightPath, 'w')
f.close()

downloadData()

workIn()
authorIsInField()
paperIsWrittenBy()
paperIsInField()
paperPublishOn()
paperCitPaper()
fieldIsPartOfField()

normalization()
