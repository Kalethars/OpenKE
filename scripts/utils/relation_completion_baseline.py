import nltk
import os
import math

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
database = 'ACE17K'
stemmer = nltk.PorterStemmer()


def coCount(data, a, b):  # One dict
    return len(data.get(a, set()) & data.get(b, set()))


def coCount2(dataA, dataB, a, b):  # Two homo dicts
    return len((dataA.get(a, set()) & dataB.get(b, set())) | (dataB.get(a, set()) & dataA.get(b, set())))


def coCount3(dataA, dataB, a, b):  # Two hetero dicts
    return len(set(dataA.get(a, set())) & set(dataB.get(b, set())))


def getLength(data, a):
    return len(data.get(a, []))


def getLengthExcluded(data, a, b):
    l = data.get(a, [])
    return len(l) - (1 if b in l else 0)


def updateMetric(metric, entityId, value):
    metric[entityId] = metric.get(entityId, 0) + value


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def averageValue(l):
    return sum(l) / len(l)


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def deStopWords(words):
    return [word for word in words if word not in nltk.corpus.stopwords.words('english')]


def handleWords(name):
    return set(map(lambda x: stemmer.stem(x), deStopWords(nltk.word_tokenize(name))))


def partitionIndex(dataA, a, b, ignore):
    count = 0
    for paperId in dataA.get(a, []):
        if paperId != ignore:
            if b in paperFields.get(paperId, set()):
                count += 1
    return count / max(min(getLengthExcluded(dataA, a, ignore), getLengthExcluded(fieldPapers, b, ignore)), 1)


def outputMetric(metricString, metric, digit=4):
    print(metricString + ':', end=' ' * (24 - len(metricString)))
    valueString = formattedRound(averageValue(metric.values()), digit)
    print(valueString)


def infoLoader():
    def loadInfos():
        global paperTitle, fieldName

        f = open(parentDir + '/data/ACE17K/info/paperInfo.data', 'r')
        s = f.read().split('\n')
        f.close()
        paperTitle = dict()
        for line in s:
            splited = line.split('\t')
            if len(splited) != 2:
                continue
            paperTitle[splited[0]] = splited[1]

        f = open(parentDir + '/data/ACE17K/info/fieldInfo.data', 'r')
        s = f.read().split('\n')
        f.close()

        fieldName = dict()
        for line in s:
            splited = line.split('\t')
            if len(splited) != 2:
                continue
            fieldName[splited[0]] = splited[1]

    def loadTriplets():
        global paperCitedPapers, paperFields, paperAuthors, paperVenues
        global authorPapers, authorInstitutes
        global fieldPapers, fieldAuthors, fieldHierarchical
        global instituteAuthors
        global venuePapers

        filePath = parentDir + '/benchmarks/%s/triplets.txt' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        paperCitedPapers = dict()
        paperFields = dict()
        paperAuthors = dict()
        paperVenues = dict()

        authorPapers = dict()
        authorInstitutes = dict()
        authorYears = dict()
        authorYears['count'] = dict()

        fieldPapers = dict()
        fieldAuthors = dict()
        fieldHierarchical = dict()

        instituteAuthors = dict()

        venuePapers = dict()

        for line in s:
            splited = line.split()
            if len(splited) != 3:
                continue
            headId = splited[0][1:]
            tailId = splited[2][1:]
            headType = splited[0][0]
            tailType = splited[2][0]
            if headType == 'p':
                if tailType == 'p':
                    addToSet(paperCitedPapers, headId, tailId)
                    addToSet(paperCitedPapers, tailId, headId)
                if tailType == 'f':
                    addToSet(paperFields, headId, tailId)
                    addToSet(fieldPapers, tailId, headId)
                if tailType == 'a':
                    addToSet(paperAuthors, headId, tailId)
                    addToSet(authorPapers, tailId, headId)
                if tailType == 'v':
                    addToSet(paperVenues, headId, tailId)
                    addToSet(venuePapers, tailId, headId)
            elif headType == 'a':
                if tailType == 'f':
                    addToSet(fieldAuthors, tailId, headId)
                if tailType == 'i':
                    addToSet(authorInstitutes, headId, tailId)
                    addToSet(instituteAuthors, tailId, headId)
            elif headType == 'f':
                if tailType == 'f':
                    addToSet(fieldHierarchical, headId, tailId)
                    addToSet(fieldHierarchical, tailId, headId)

        for authorId in authorYears.keys():
            if authorId != 'count':
                authorYears[authorId] /= authorYears['count'][authorId]
        del authorYears['count']

    def loadPaperInstitutes():
        global paperInstitutes, institutePapers

        filePath = parentDir + '/data/%s/PaperAuthorAffiliations.data' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        paperInstitutes = dict()
        for line in s:
            splited = line.split()
            if len(splited) != 4:
                continue
            paperId = splited[0]
            instituteId = splited[2]
            if paperId == 'None' or instituteId == 'None':
                continue
            addToSet(paperInstitutes, paperId, instituteId)
            addToSet(institutePapers, instituteId, paperId)

    def calcSecondaryCounts():
        global authorVenues, venueAuthors, fieldAuthors, fieldVenues
        global authorFieldsCount, instituteFieldsCount, venueFieldsCount
        global authorCitedPapers, fieldCitedPapers, instituteCitedPapers, venueCitedPapers
        global authorCoAuthors

        authorVenues = dict()
        venueAuthors = dict()
        # fieldAuthors = dict()
        authorFieldsCount = dict()
        authorCitedPapers = dict()
        for authorId in authorPapers.keys():
            authorFieldsCount[authorId] = dict()
            for paperId in authorPapers[authorId]:
                addToSet(authorCitedPapers, authorId, paperCitedPapers.get(paperId, set()))
                for venueId in paperVenues.get(paperId, set()):
                    addToSet(authorVenues, authorId, venueId)
                    addToSet(venueAuthors, venueId, authorId)
                for fieldId in paperFields.get(paperId, set()):
                    addToSet(fieldAuthors, fieldId, authorId)
                    updateMetric(authorFieldsCount[authorId], fieldId, 1)

        for fieldId in fieldAuthors.keys():
            for authorId in fieldAuthors[fieldId]:
                if authorId in authorFieldsCount:
                    if authorFieldsCount[authorId].get(fieldId, 0) == 0:
                        authorFieldsCount[authorId][fieldId] = 1
                else:
                    authorFieldsCount[authorId] = dict()
                    authorFieldsCount[authorId][fieldId] = 1

        fieldCitedPapers = dict()
        for fieldId in fieldPapers.keys():
            for paperId in fieldPapers[fieldId]:
                addToSet(fieldCitedPapers, fieldId, paperCitedPapers.get(paperId, set()))

        instituteFieldsCount = dict()
        instituteCitedPapers = dict()
        for instituteId in institutePapers.keys():
            instituteFieldsCount[instituteId] = dict()
            for paperId in institutePapers[instituteId]:
                addToSet(instituteCitedPapers, instituteId, paperCitedPapers.get(paperId, set()))
                for fieldId in paperFields.get(paperId, set()):
                    updateMetric(instituteFieldsCount[instituteId], fieldId, 1)

        fieldVenues = dict()
        venueFieldsCount = dict()
        venueCitedPapers = dict()
        for venueId in venuePapers.keys():
            venueFieldsCount[venueId] = dict()
            for paperId in venuePapers[venueId]:
                addToSet(venueCitedPapers, venueId, paperCitedPapers.get(paperId, set()))
                for fieldId in paperFields.get(paperId, set()):
                    addToSet(fieldVenues, fieldId, venueId)
                    updateMetric(venueFieldsCount[venueId], fieldId, 1)

        authorCoAuthors = dict()
        for paperId in paperAuthors.keys():
            for authorId1 in paperAuthors[paperId]:
                for authorId2 in paperAuthors[paperId]:
                    if authorId1 < authorId2:
                        addToSet(authorCoAuthors, authorId1, authorId2)
                        addToSet(authorCoAuthors, authorId2, authorId1)

    loadInfos()
    loadTriplets()
    loadPaperInstitutes()
    calcSecondaryCounts()


paperCitedPapers = dict()
paperFields = dict()
paperAuthors = dict()
paperVenues = dict()
paperInstitutes = dict()

authorPapers = dict()
authorInstitutes = dict()
authorVenues = dict()
authorFieldsCount = dict()
authorCitedPapers = dict()
authorCoAuthors = dict()

fieldPapers = dict()
fieldAuthors = dict()
fieldVenues = dict()
fieldCitedPapers = dict()
fieldHierarchical = dict()

instituteAuthors = dict()
institutePapers = dict()
instituteFieldsCount = dict()
instituteCitedPapers = dict()

venuePapers = dict()
venueAuthors = dict()
venueFieldsCount = dict()
venueCitedPapers = dict()

infoLoader()

paperIndex = dict()
authorIndex = dict()
venueIndex = dict()
instituteIndex = dict()
wordIndex = dict()

count = 0
for paperId in paperFields.keys():
    count += 1

    pIndex = 0
    aIndex = 0
    vIndex = 0
    iIndex = 0
    wIndex = 0
    for fieldId in paperFields[paperId]:
        pIndex += partitionIndex(paperCitedPapers, paperId, fieldId, paperId)
        for authorId in paperAuthors.get(paperId, []):
            aIndex += partitionIndex(authorPapers, authorId, fieldId, paperId)
        for venueId in paperVenues.get(paperId, []):
            vIndex += partitionIndex(venuePapers, venueId, fieldId, paperId)
        for instituteId in paperInstitutes.get(paperId, []):
            iIndex += partitionIndex(institutePapers, instituteId, fieldId, paperId)

        paperTitleStems = handleWords(paperTitle[paperId])
        fieldNameStems = handleWords(fieldName[fieldId])
        wIndex += min(math.sqrt(len(paperTitleStems & fieldNameStems) /
                                min(max(len(fieldNameStems), 1), 3)), 1)
    length = len(paperFields[paperId])
    if length > 0:
        paperIndex[paperId] = pIndex / length
        authorIndex[paperId] = aIndex / length
        venueIndex[paperId] = vIndex / length
        instituteIndex[paperId] = iIndex / length
        wordIndex[paperId] = wIndex / length

    if int(count * 100 / len(paperFields)) > int((count - 1) * 100 / len(paperFields)):
        print(str(int(count * 100 / len(paperFields))) + '%')
        outputMetric('Paper Index', paperIndex)
        outputMetric('Author Index', authorIndex)
        outputMetric('Venue Index', venueIndex)
        outputMetric('Institute Index', instituteIndex)
        outputMetric('Word Index', wordIndex)
