# -*- coding: UTF-8 -*-

import pymysql
import argparse
import os


def connectSQL(config):
    if config.get('charset', 0) != 0:
        conn = pymysql.connect(host=config['host'], port=int(config['port']), user=config['user'],
                               passwd=config['passwd'], db=config['db'], charset=config['charset'])
    else:
        conn = pymysql.connect(host=config['host'], port=int(config['port']), user=config['user'],
                               passwd=config['passwd'], db=config['db'])
    return conn


def disconnectSQL(conn):
    conn.commit()
    conn.close()


def loadConfig(configName):
    f = open('../' + configName + '.config')
    s = f.read().split('\n')
    f.close()
    config = dict()
    for line in s:
        splited = line.split('=')
        if len(splited) == 2:
            config[splited[0]] = splited[1]
    return config


def parseParams(line):
    paramMap = dict()
    splitedLine = line.split()
    for each in splitedLine:
        pos = each.find('=')
        if pos >= 0:
            paramMap[each[:pos]] = each[pos + 1:]

    return paramMap


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=True)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parsedArgs = parser.parse_args()

database = parsedArgs.database
method = parsedArgs.method
order = parsedArgs.order

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

f = open(parentDir + '/benchmarks/' + database + '/entity2id.txt', 'r')
s = f.read().split('\n')
f.close()
venues = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    if splited[0][0] == 'v':
        venues[int(splited[1])] = splited[0][1:]

f = open(parentDir + '/scripts/config/' + method + '.config', 'r')
s = f.read().split('\n')
f.close()
parsedParams = parseParams(s[order])

resultPath = parentDir + '/res/' + database + '/' + method + '/' + str(order) + '/'
f = open(resultPath + 'embedding.vec.json', 'r')
s = f.read().split('"ent_embeddings": [')[1].split('}')[0].split('], ')
f.close()

vectors = dict()
for i in range(len(s)):
    if not i in venues.keys():
        continue
    line = s[i][1:]
    splited = line.split(', ')
    if len(splited) != int(parsedParams['dimension']):
        continue
    vectors[i] = splited

databaseConfig = loadConfig('database')
databaseConfig2 = loadConfig('database2')
conn = connectSQL(databaseConfig)
cursor = conn.cursor()
conn2 = connectSQL(databaseConfig2)
cursor2 = conn2.cursor()
f = open(resultPath + 'venue_index.txt', 'w')
g = open(resultPath + 'venue_data.txt', 'w')
for key in venues.keys():
    venueId = venues[key]
    vector = vectors[key]
    f.write(venueId + '\t')
    query = 'select ShortName from ConferenceSeries where ConferenceSeriesID="' + venueId + '"'
    cursor.execute(query)
    tmp = cursor.fetchall()
    if len(tmp) > 0:
        f.write('Conference\t' + tmp[0][0].replace(' ', '') + '\t')
        query = 'select FieldNameEnglish,FieldOrder from CCFConference where ConfID="' + venueId + '"'
        cursor2.execute(query)
        tmp = cursor2.fetchall()
        f.write(tmp[0][0].replace(' ', '.') + '\t' + str(tmp[0][1]) + '\n')
        for i in range(len(vector)):
            g.write(str(vector[i]))
            if i < len(vector) - 1:
                g.write('\t')
        g.write('\n')
        continue
    query = 'select JourShortNames from CCFJournal where JourID="' + venueId + '"'
    cursor2.execute(query)
    tmp = cursor2.fetchall()
    if len(tmp[0][0].replace(' ', '')) == 0:
        query = 'select JourFullName from CCFJournal where JourID="' + venueId + '"'
        cursor2.execute(query)
        tmp = cursor2.fetchall()
    f.write('Journal\t' + tmp[0][0].replace(' ', '') + '\t')
    query = 'select FieldNameEnglish,FieldOrder from CCFJournal where JourID="' + venueId + '"'
    cursor2.execute(query)
    tmp = cursor2.fetchall()
    f.write(tmp[0][0].replace(' ', '.') + '\t' + str(tmp[0][1]) + '\n')
    for i in range(len(vector)):
        g.write(str(vector[i]))
        if i < len(vector) - 1:
            g.write('\t')
    g.write('\n')
f.close()
g.close()
disconnectSQL(conn)
disconnectSQL(conn2)
