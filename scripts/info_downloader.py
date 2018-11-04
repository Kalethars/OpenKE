# -*- coding: UTF-8 -*-

import pymysql
import argparse
import os
import win_unicode_console

win_unicode_console.enable()


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


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
    global parentDir
    f = open(parentDir + '/scripts/' + configName + '.config', 'r')
    s = f.read().split('\n')
    f.close()
    config = dict()
    for line in s:
        splited = line.split('=')
        if len(splited) == 2:
            config[splited[0]] = splited[1]
    return config


def safeString(s):
    replacement = [(8211, '-')]

    s = s.encode('gbk', 'ignore').decode('gbk')
    for (value, char) in replacement:
        s = s.replace(chr(value), char)
    s = ' '.join(s.split()).strip()
    return s


def capitalize(s):
    ignoreCases = {'in', 'of', 'and'}

    if len(s) == 0:
        return s

    words = s.split()
    for i in range(len(words)):
        if not words[i] in ignoreCases:
            words[i] = str.capitalize(words[i])
    return ' '.join(words)


def venueDownloader(entities):
    databaseConfig = loadConfig('database')
    databaseConfig2 = loadConfig('database2')
    conn = connectSQL(databaseConfig)
    cursor = conn.cursor()
    conn2 = connectSQL(databaseConfig2)
    cursor2 = conn2.cursor()

    infoSavePath = infoSaveDir + 'venueInfo.data'
    if not update:
        if os.path.exists(infoSavePath):
            return

    f = open(infoSavePath, 'w')
    print('Downloading venue info...')
    print(len(entities))
    count = 0
    for key in entities.keys():
        count += 1
        if int(count * 100 / len(entities)) > int((count - 1) * 100 / len(entities)):
            print(str(int(count * 100 / len(entities))) + '%')

        venueId = entities[key]
        f.write(venueId + '\t')
        query = 'select ShortName from ConferenceSeries where ConferenceSeriesID="' + venueId + '"'
        cursor.execute(query)
        tmp = cursor.fetchall()
        if len(tmp) > 0:
            f.write('Conference\t' + safeString(tmp[0][0]).replace(' ', '') + '\t')
            query = 'select FieldNameEnglish,FieldOrder from CCFConference where ConfID="' + venueId + '"'
            cursor2.execute(query)
            tmp = cursor2.fetchall()
            f.write(safeString(tmp[0][0]).replace(' ', '.') + '\t' + str(tmp[0][1]) + '\n')
            continue
        query = 'select JourShortNames from CCFJournal where JourID="' + venueId + '"'
        cursor2.execute(query)
        tmp = cursor2.fetchall()
        if len(safeString(tmp[0][0]).replace(' ', '')) == 0:
            query = 'select JourFullName from CCFJournal where JourID="' + venueId + '"'
            cursor2.execute(query)
            tmp = cursor2.fetchall()
        f.write('Journal\t' + safeString(tmp[0][0]).replace(' ', '') + '\t')
        query = 'select FieldNameEnglish,FieldOrder from CCFJournal where JourID="' + venueId + '"'
        cursor2.execute(query)
        tmp = cursor2.fetchall()
        f.write(safeString(tmp[0][0]).replace(' ', '.') + '\t' + str(tmp[0][1]) + '\n')
    f.close()

    disconnectSQL(conn)
    disconnectSQL(conn2)


def paperDownloader(entities):
    databaseConfig = loadConfig('database')
    conn = connectSQL(databaseConfig)
    cursor = conn.cursor()

    infoSavePath = infoSaveDir + 'paperInfo.data'
    if not update:
        if os.path.exists(infoSavePath):
            return

    f = open(infoSavePath, 'w')
    print('Downloading paper info...')
    print(len(entities))
    count = 0
    for key in entities.keys():
        count += 1
        if int(count * 100 / len(entities)) > int((count - 1) * 100 / len(entities)):
            print(str(int(count * 100 / len(entities))) + '%')

        paperId = entities[key]
        query = 'select OriginalPaperTitle from Papers where PaperID="' + paperId + '"'
        cursor.execute(query)
        tmp = cursor.fetchall()
        if len(tmp) > 0:
            f.write(paperId + '\t' + safeString(tmp[0][0]) + '\n')
    f.close()

    disconnectSQL(conn)


def authorDownloader(entities):
    databaseConfig = loadConfig('database')
    conn = connectSQL(databaseConfig)
    cursor = conn.cursor()

    infoSavePath = infoSaveDir + 'authorInfo.data'
    if not update:
        if os.path.exists(infoSavePath):
            return

    f = open(infoSavePath, 'w')
    print('Downloading author info...')
    print(len(entities))
    count = 0
    for key in entities.keys():
        count += 1
        if int(count * 100 / len(entities)) > int((count - 1) * 100 / len(entities)):
            print(str(int(count * 100 / len(entities))) + '%')

        authorId = entities[key]
        query = 'select AuthorName from Authors where AuthorID="' + authorId + '"'
        cursor.execute(query)
        tmp = cursor.fetchall()
        if len(tmp) > 0:
            f.write(authorId + '\t' + capitalize(safeString(tmp[0][0])) + '\n')
    f.close()

    disconnectSQL(conn)


def instituteDownloader(entities):
    databaseConfig = loadConfig('database')
    conn = connectSQL(databaseConfig)
    cursor = conn.cursor()

    infoSavePath = infoSaveDir + 'instituteInfo.data'
    if not update:
        if os.path.exists(infoSavePath):
            return

    f = open(infoSavePath, 'w')
    print('Downloading institute info...')
    print(len(entities))
    count = 0
    for key in entities.keys():
        count += 1
        if int(count * 100 / len(entities)) > int((count - 1) * 100 / len(entities)):
            print(str(int(count * 100 / len(entities))) + '%')

        instituteId = entities[key]
        query = 'select AffiliationName from Affiliations where AffiliationID="' + instituteId + '"'
        cursor.execute(query)
        tmp = cursor.fetchall()
        if len(tmp) > 0:
            f.write(instituteId + '\t' + capitalize(safeString(tmp[0][0])) + '\n')
    f.close()

    disconnectSQL(conn)


def fieldDownloader(entities):
    databaseConfig = loadConfig('database')
    conn = connectSQL(databaseConfig)
    cursor = conn.cursor()

    infoSavePath = infoSaveDir + 'fieldInfo.data'
    if not update:
        if os.path.exists(infoSavePath):
            return

    f = open(infoSavePath, 'w')
    print('Downloading field info...')
    print(len(entities))
    count = 0
    for key in entities.keys():
        count += 1
        if int(count * 100 / len(entities)) > int((count - 1) * 100 / len(entities)):
            print(str(int(count * 100 / len(entities))) + '%')

        fieldId = entities[key]
        query = 'select FieldsOfStudyName from FieldsOfStudy where FieldsOfStudyID="' + fieldId + '"'
        cursor.execute(query)
        tmp = cursor.fetchall()
        if len(tmp) > 0:
            f.write(fieldId + '\t' + capitalize(safeString(tmp[0][0])) + '\n')
    f.close()

    disconnectSQL(conn)


types = ['paper', 'author', 'institute', 'field', 'venue']

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=True)
parser.add_argument('--update', type=bool, required=False)
parser.add_argument('--target', type=str, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database
update = parsedArgs.update if parsedArgs.update else False
target = parsedArgs.target.lower() if parsedArgs.target else None

if target != None:
    if not target in types:
        raise ValueError('Invalid target! Must be one of {' + ', '.join(types) + '}.')

parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

f = open(parentDir + '/benchmarks/' + database + '/entity2id.txt', 'r')
s = f.read().split('\n')
f.close()

allEntities = dict()
for type in types:
    allEntities[type] = dict()

for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    for type in types:
        if splited[0][0] == type[0]:
            allEntities[type][int(splited[1])] = splited[0][1:]

mkdir(['data', database, 'info'])
infoSaveDir = parentDir + '/data/' + database + '/info/'

if target != None:
    exec(target + 'Downloader(allEntities["' + target + '"])')
else:
    for type in types:
        exec(type + 'Downloader(allEntities["' + type + '"])')
