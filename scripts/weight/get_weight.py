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
            triplets[int(splited[0])].append([splited[1][1:], splited[2][1:]])


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


def fieldIsPartOfField():
    # relation = 6, head = field, tail = field
    def downloadData():
        f = open(getDataPath(filename), 'w')

        conn = connectSQL()
        cursor = conn.cursor()
        for entities in triplets[6]:
            query = 'select ChildFieldOfStudyID, ParentFieldOfStudyID, Confidence from FieldOfStudyHierarchy \
                where ChildFieldOfStudyID="%(head)s" and ParentFieldOfStudyID="%(tail)s"' \
                    % {'head': entities[0], 'tail': entities[1]}
            cursor.execute(query)
            results = cursor.fetchall()
            for each in results:
                f.write('\t'.join(map(lambda x: str(x), each)) + '\n')

        f.close()

    filename = 'field_is_part_of_field.data'
    data = loadData(filename)
    if data is None:
        downloadData()
        data = loadData(filename)
    f = open(weightPath, 'a')
    for line in data:
        f.write('6 f%(head)s f%(tail)s %(confidence)s\n' % {'head': line[0], 'tail': line[1], 'confidence': line[2]})
    f.close()


config = dict()
loadConfig()
triplets = [[] for i in range(7)]
loadTriplets()

weightPath = parentDir + '/benchmarks/ACE17K/triplets_weight.txt'
f = open(weightPath, 'w')
f.close()

fieldIsPartOfField()
