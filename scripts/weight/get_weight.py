import os

import pymysql

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


def loadTriplets():
    # triplets[relation]=list of [head, tail]

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


def paperIsWrittenBy():
    # relaation = 2, head = paper, tail = author
    def downloadData():
        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for triplet in triplets[3]:
            query = 'select PaperId, AuthorId, AffiliationId, AuthorSequenceNumber from PaperAuthorAffiliations \
                     where PaperId="%(head)s" and AuthorId="%(tail)s"' \
                    % {'head': triplet[0][1:], 'tail': triplet[1][1:]}
            cursor.execute(query)
            results = cursor.fetchall
            for result in results:
                f.write('\t'.join(map(lambda x: str(x), result)) + '\n')
        disconnectSQL(conn)

        f.close()

    filename = 'PaperAuthorAffiliations.data'
    data = loadData(filename)
    if data is None:
        downloadData()
        data = loadData(filename)
    f = open(weightPath, 'a')
    for line in data:
        f.write(buildWeightString(3, 'p' + line[0], 'a' + line[1], line[3]))


def paperIsInField():
    # relation = 3, head = paper, tail = field
    f = open(weightPath, 'a')
    for triplet in triplets[3]:
        f.write(buildWeightString(3, triplet[0], triplet[1], 1))


def fieldIsPartOfField():
    # relation = 6, head = field, tail = field
    def downloadData():
        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for triplet in triplets[6]:
            query = 'select ChildFieldOfStudyID, ParentFieldOfStudyID, Confidence from FieldOfStudyHierarchy \
                     where ChildFieldOfStudyID="%(head)s" and ParentFieldOfStudyID="%(tail)s"' \
                    % {'head': triplet[0][1:], 'tail': triplet[1][1:]}
            cursor.execute(query)
            results = cursor.fetchall()
            for result in results:
                f.write('\t'.join(map(lambda x: str(x), result)) + '\n')
        disconnectSQL(conn)

        f.close()

    filename = 'FieldOfStudyHierarchy.data'
    data = loadData(filename)
    if data is None:
        downloadData()
        data = loadData(filename)
    f = open(weightPath, 'a')
    for line in data:
        f.write(buildWeightString(6, 'f' + line[0], 'f' + line[1], line[2]))
    f.close()


config = dict()
loadConfig()
triplets = [[] for i in range(7)]
loadTriplets()

weightPath = parentDir + '/benchmarks/ACE17K/triplets_weight.txt'
f = open(weightPath, 'w')
f.close()

paperIsWrittenBy()
paperIsInField()
fieldIsPartOfField()
