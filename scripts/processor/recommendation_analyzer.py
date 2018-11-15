import argparse
import os
import math
import win_unicode_console

win_unicode_console.enable()

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

hitAt = [10, 3, 1]


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def output(f, s='', end='\n'):
    print(s + end, end='')
    if not f is None:
        f.write(s + end)


def outputMetric(metricString, metric, digit=4):
    output(logFile, metricString + ':', end=' ' * (24 - len(metricString)))
    for num in sorted(metric.keys(), reverse=True):
        valueString = formattedRound(averageValue(metric[num].values()), digit)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def coCount(data, a, b):
    return len(data.get(a, set()) & data.get(b, set()))


def coCount2(dataA, dataB, a, b):
    return len((dataA.get(a, set()) & dataB.get(b, set())) | (dataB.get(a, set()) & dataA.get(b, set())))


def getLength(data, a):
    return len(data.get(a, []))


def minSum(data, a, b):
    dataA = data.get(a, dict())
    dataB = data.get(b, dict())
    s = 0
    for key in dataA.keys():
        s += min(dataA[key], dataB.get(key, 0))
    return s


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


def infoLoader():
    def loadPaperYears():
        global paperYears

        filePath = parentDir + '/data/%s/PaperYears.data' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        paperYears = dict()
        for line in s:
            splited = line.split()
            if len(splited) != 2:
                continue
            paperId = splited[0]
            year = int(splited[1])
            paperYears[paperId] = year

    def loadPaperCitations():
        global paperCitations

        filePath = parentDir + '/data/%s/PaperCitations.data' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        paperCitations = dict()
        for line in s:
            splited = line.split()
            if len(splited) != 2:
                continue
            paperId = splited[0]
            citationCount = int(splited[1])
            paperCitations[paperId] = citationCount

    def loadTriplets():
        global paperCitedPapers, paperFields, paperAuthors, paperVenues
        global authorPapers, authorInstitutes, authorYears
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
                    updateMetric(authorYears, tailId, paperYears[headId])
                    updateMetric(authorYears['count'], tailId, 1)
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
        global authorVenues, venueAuthors, fieldAuthors
        global authorFieldsCount, instituteFieldsCount, venueFieldsCount
        global authorCitedPapers, fieldCitedPapers, instituteCitedPapers, venueCitedPapers

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

        venueFieldsCount = dict()
        venueCitedPapers = dict()
        for venueId in venuePapers.keys():
            venueFieldsCount[venueId] = dict()
            for paperId in venuePapers[venueId]:
                addToSet(venueCitedPapers, venueId, paperCitedPapers.get(paperId, set()))
                for fieldId in paperFields.get(paperId, set()):
                    updateMetric(venueFieldsCount[venueId], fieldId, 1)

    def loadVenueName():
        global venueName

        filePath = parentDir + '/data/%s/info/venueInfo.data' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        venueName = dict()
        for line in s:
            splited = line.split()
            if len(splited) == 5:
                venueName[splited[0]] = splited[2]

    loadPaperYears()
    loadPaperCitations()
    loadTriplets()
    loadPaperInstitutes()
    calcSecondaryCounts()
    loadVenueName()


def paperRecommendationAnalyzer():
    def paperProperties(recommendationId, paperId):
        if recommendationId == paperId:
            properties = [
                ('Year', paperYears[paperId]),
                ('Citation', paperCitations[paperId]),
                ('Cite & Cited by', getLength(paperCitedPapers, paperId)),
                ('Fields', getLength(paperFields, paperId)),
                ('Authors', getLength(paperAuthors, paperId)),
                ('Venue', '/'.join(list(map(lambda x: venueName[x], paperVenues.get(paperId, []))))),
                ('Institutes', getLength(paperInstitutes, paperId))
            ]
        else:
            properties = [
                ('Year', paperYears[recommendationId]),
                ('Citation', paperCitations[recommendationId]),
                ('Co-cites', coCount(paperCitedPapers, paperId, recommendationId) +
                             1 if recommendationId in paperCitedPapers.get(paperId, set()) else 0),
                ('Co-fields', coCount(paperFields, paperId, recommendationId)),
                ('Co-authors', coCount(paperAuthors, paperId, recommendationId)),
                ('Co-venues', coCount(paperVenues, paperId, recommendationId)),
                ('Co-institutes', coCount(paperInstitutes, paperId, recommendationId))
            ]
        return '\t'.join([properties[i][0] + ': ' + str(properties[i][1]) for i in range(len(properties))])

    filePath = recommendationDir + 'paper' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    analyzedFilePath = recommendationDir + '/analyzed/paper' + filenameSuffix
    f = open(analyzedFilePath, 'w')

    paperRecommendation = dict()
    paperIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            paperId = s[i - 1].split()[1]
            paperIdSorted.append(paperId)

            f.write(s[i - 1] + '\n')
            f.write(paperProperties(paperId, paperId) + '\n')
            f.write('-' * 50 + '\n')

            paperRecommendation[paperId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 2:
                    continue
                recommendationId = splited[0]
                paperRecommendation[paperId].append(recommendationId)

                f.write(s[i + j + 1] + '\n')
                f.write(paperProperties(recommendationId, paperId) + '\n')

            f.write('\n')

    f.close()

    avgYearDiff = dict()
    avgYearDiffAbs = dict()
    avgCiteDiff = dict()
    avgCoCite = dict()
    avgCoField = dict()
    avgCoAuthor = dict()
    avgCoVenue = dict()
    avgCoInstitute = dict()
    for num in hitAt:
        avgYearDiff[num] = dict()
        avgYearDiffAbs[num] = dict()
        avgCiteDiff[num] = dict()
        avgCoCite[num] = dict()
        avgCoField[num] = dict()
        avgCoAuthor[num] = dict()
        avgCoVenue[num] = dict()
        avgCoInstitute[num] = dict()
    for paperId in paperIdSorted:
        recommendationList = paperRecommendation[paperId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgYearDiff[num], paperId, paperYears[recommendationId] - paperYears[paperId])
                    updateMetric(avgYearDiffAbs[num], paperId, abs(paperYears[recommendationId] - paperYears[paperId]))
                    updateMetric(avgCiteDiff[num], paperId, paperCitations[recommendationId] - paperCitations[paperId])
                    updateMetric(avgCoCite[num], paperId, coCount(paperCitedPapers, paperId, recommendationId))
                    if recommendationId in paperCitedPapers.get(paperId, set()):
                        updateMetric(avgCoCite[num], paperId, 1)
                    updateMetric(avgCoField[num], paperId, coCount(paperFields, paperId, recommendationId))
                    updateMetric(avgCoAuthor[num], paperId, coCount(paperAuthors, paperId, recommendationId))
                    updateMetric(avgCoVenue[num], paperId, coCount(paperVenues, paperId, recommendationId))
                    updateMetric(avgCoInstitute[num], paperId, coCount(paperInstitutes, paperId, recommendationId))

        for num in hitAt:
            avgYearDiff[num][paperId] /= num
            avgYearDiffAbs[num][paperId] /= num
            avgCiteDiff[num][paperId] /= num
            avgCoCite[num][paperId] /= num
            avgCoField[num][paperId] /= num
            avgCoAuthor[num][paperId] /= num
            avgCoVenue[num][paperId] /= num
            avgCoInstitute[num][paperId] /= num

    output(logFile, ' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)
    outputMetric('Average Year Diff', avgYearDiff)
    outputMetric('Average Year Diff Abs', avgYearDiffAbs)
    outputMetric('Average Citation Diff', avgCiteDiff)
    outputMetric('Average Co-cites', avgCoCite)
    outputMetric('Average Co-fields', avgCoField)
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-venues', avgCoVenue)
    outputMetric('Average Co-institutes', avgCoInstitute)
    output(logFile)


def authorRecommendationAnalyzer():
    def authorProperties(recommendationId, authorId):
        if recommendationId == authorId:
            properties = [
                ('Year', formattedRound(authorYears[authorId], 2)),
                ('Papers', getLength(authorPapers, authorId)),
                ('Institutes', getLength(authorInstitutes, authorId)),
                ('Venues', getLength(authorVenues, authorId)),
                ('Fields', getLength(authorFieldsCount, authorId)),
                ('Cite & Cited by', getLength(authorCitedPapers, authorId))
            ]
        else:
            properties = [
                ('Year', formattedRound(authorYears[recommendationId], 2)),
                ('Co-papers', coCount(authorPapers, authorId, recommendationId)),
                ('Co-institutes', coCount(authorInstitutes, authorId, recommendationId)),
                ('Co-venues', coCount(authorVenues, authorId, recommendationId)),
                ('Co-fields-count', minSum(authorFieldsCount, authorId, recommendationId)),
                ('Co-cites', coCount2(authorCitedPapers, authorPapers, authorId, recommendationId))
            ]
        return '\t'.join([properties[i][0] + ': ' + str(properties[i][1]) for i in range(len(properties))])

    filePath = recommendationDir + 'author' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    analyzedFilePath = recommendationDir + '/analyzed/author' + filenameSuffix
    f = open(analyzedFilePath, 'w')

    authorRecommendation = dict()
    authorIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            authorId = s[i - 1].split()[1]
            authorIdSorted.append(authorId)

            f.write(s[i - 1] + '\n')
            f.write(authorProperties(authorId, authorId) + '\n')
            f.write('-' * 50 + '\n')

            authorRecommendation[authorId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 2:
                    continue
                recommendationId = splited[0]
                authorRecommendation[authorId].append(recommendationId)

                f.write(s[i + j + 1] + '\n')
                f.write(authorProperties(recommendationId, authorId) + '\n')

            f.write('\n')

    f.close()

    avgYearDiff = dict()
    avgYearDiffAbs = dict()
    avgCoPaper = dict()
    avgCoInstitute = dict()
    avgCoVenue = dict()
    avgCoFieldCount = dict()
    avgCoCite = dict()
    for num in hitAt:
        avgYearDiff[num] = dict()
        avgYearDiffAbs[num] = dict()
        avgCoPaper[num] = dict()
        avgCoInstitute[num] = dict()
        avgCoVenue[num] = dict()
        avgCoFieldCount[num] = dict()
        avgCoCite[num] = dict()
    for authorId in authorIdSorted:
        recommendationList = authorRecommendation[authorId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgYearDiff[num], authorId, authorYears[recommendationId] - authorYears[authorId])
                    updateMetric(avgYearDiffAbs[num], authorId,
                                 abs(authorYears[recommendationId] - authorYears[authorId]))
                    updateMetric(avgCoPaper[num], authorId, coCount(authorPapers, authorId, recommendationId))
                    updateMetric(avgCoInstitute[num], authorId, coCount(authorInstitutes, authorId, recommendationId))
                    updateMetric(avgCoFieldCount[num], authorId, minSum(authorFieldsCount, authorId, recommendationId))
                    updateMetric(avgCoVenue[num], authorId, coCount(authorVenues, authorId, recommendationId))
                    updateMetric(avgCoCite[num], authorId,
                                 coCount2(authorCitedPapers, authorPapers, authorId, recommendationId))

        for num in hitAt:
            avgYearDiff[num][authorId] /= num
            avgYearDiffAbs[num][authorId] /= num
            avgCoPaper[num][authorId] /= num
            avgCoInstitute[num][authorId] /= num
            avgCoVenue[num][authorId] /= num
            avgCoFieldCount[num][authorId] /= num
            avgCoCite[num][authorId] /= num

    output(logFile, ' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)
    outputMetric('Average Year Diff', avgYearDiff)
    outputMetric('Average Year Diff Abs', avgYearDiffAbs)
    outputMetric('Average Co-papers', avgCoPaper)
    outputMetric('Average Co-institutes', avgCoInstitute)
    outputMetric('Average Co-venues', avgCoVenue)
    outputMetric('Average Co-fields-count', avgCoFieldCount)
    outputMetric('Average Co-cites', avgCoCite)
    output(logFile)


def fieldRecommendationAnalyzer():
    def fieldProperties(recommendationId, fieldId):
        if recommendationId == fieldId:
            properties = [
                ('Papers', getLength(fieldPapers, fieldId)),
                ('Authors', getLength(fieldAuthors, fieldId)),
                ('Hierarchical Fields', getLength(fieldHierarchical, fieldId)),
                ('Cite & Cited by', getLength(fieldCitedPapers, fieldId))
            ]
        else:
            properties = [
                ('Co-papers', coCount(fieldPapers, fieldId, recommendationId)),
                ('Co-authors', coCount(fieldAuthors, fieldId, recommendationId)),
                ('Related Fields', coCount(fieldHierarchical, fieldId, recommendationId) +
                                   1 if recommendationId in fieldHierarchical.get(fieldId, set()) else 0),
                ('Co-cites', coCount2(fieldCitedPapers, fieldPapers, fieldId, recommendationId))
            ]
        return '\t'.join([properties[i][0] + ': ' + str(properties[i][1]) for i in range(len(properties))])

    filePath = recommendationDir + 'field' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    analyzedFilePath = recommendationDir + '/analyzed/field' + filenameSuffix
    f = open(analyzedFilePath, 'w')

    fieldRecommendation = dict()
    fieldIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            fieldId = s[i - 1].split()[1]
            fieldIdSorted.append(fieldId)

            f.write(s[i - 1] + '\n')
            f.write(fieldProperties(fieldId, fieldId) + '\n')
            f.write('-' * 50 + '\n')

            fieldRecommendation[fieldId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 2:
                    continue
                recommendationId = splited[0]
                fieldRecommendation[fieldId].append(recommendationId)

                f.write(s[i + j + 1] + '\n')
                f.write(fieldProperties(recommendationId, fieldId) + '\n')

            f.write('\n')

    f.close()

    avgCoPaper = dict()
    avgCoAuthor = dict()
    avgCoField = dict()
    avgCoCite = dict()
    for num in hitAt:
        avgCoPaper[num] = dict()
        avgCoAuthor[num] = dict()
        avgCoField[num] = dict()
        avgCoCite[num] = dict()
    for fieldId in fieldIdSorted:
        recommendationList = fieldRecommendation[fieldId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoPaper[num], fieldId, coCount(fieldPapers, fieldId, recommendationId))
                    updateMetric(avgCoAuthor[num], fieldId, coCount(fieldAuthors, fieldId, recommendationId))
                    updateMetric(avgCoField[num], fieldId, coCount(fieldHierarchical, fieldId, recommendationId))
                    if recommendationId in fieldHierarchical.get(fieldId, set()):
                        updateMetric(avgCoField[num], fieldId, 1)
                    updateMetric(avgCoCite[num], fieldId,
                                 coCount2(fieldCitedPapers, fieldPapers, fieldId, recommendationId))

        for num in hitAt:
            avgCoPaper[num][fieldId] /= num
            avgCoAuthor[num][fieldId] /= num
            avgCoField[num][fieldId] /= num
            avgCoCite[num][fieldId] /= num

    output(logFile, ' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)
    outputMetric('Average Co-papers', avgCoPaper)
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-fields', avgCoField)
    outputMetric('Average Co-cites', avgCoCite)
    output(logFile)


def instituteRecommendationAnalyzer():
    def instituteProperties(recommendationId, instituteId):
        if recommendationId == instituteId:
            properties = [
                ('Authors', getLength(instituteAuthors, instituteId)),
                ('Papers', getLength(institutePapers, instituteId)),
                ('Fields', getLength(instituteFieldsCount, instituteId)),
                ('Cite & Cited by', getLength(instituteCitedPapers, instituteId))
            ]
        else:
            properties = [
                ('Co-authors', coCount(instituteAuthors, instituteId, recommendationId)),
                ('Co-papers', coCount(institutePapers, instituteId, recommendationId)),
                ('Co-fields-count', minSum(instituteFieldsCount, instituteId, recommendationId)),
                ('Co-cites', coCount2(instituteCitedPapers, institutePapers, instituteId, recommendationId))
            ]
        return '\t'.join([properties[i][0] + ': ' + str(properties[i][1]) for i in range(len(properties))])

    filePath = recommendationDir + 'institute' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    analyzedFilePath = recommendationDir + '/analyzed/institute' + filenameSuffix
    f = open(analyzedFilePath, 'w')

    instituteRecommendation = dict()
    instituteIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            instituteId = s[i - 1].split()[1]
            instituteIdSorted.append(instituteId)

            f.write(s[i - 1] + '\n')
            f.write(instituteProperties(instituteId, instituteId) + '\n')
            f.write('-' * 50 + '\n')

            instituteRecommendation[instituteId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 2:
                    continue
                recommendationId = splited[0]
                instituteRecommendation[instituteId].append(recommendationId)

                f.write(s[i + j + 1] + '\n')
                f.write(instituteProperties(recommendationId, instituteId) + '\n')

            f.write('\n')

    f.close()

    avgCoAuthor = dict()
    avgCoPaper = dict()
    avgCoFieldCount = dict()
    avgCoCite = dict()
    for num in hitAt:
        avgCoAuthor[num] = dict()
        avgCoPaper[num] = dict()
        avgCoFieldCount[num] = dict()
        avgCoCite[num] = dict()
    for instituteId in instituteIdSorted:
        recommendationList = instituteRecommendation[instituteId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoAuthor[num], instituteId,
                                 coCount(instituteAuthors, instituteId, recommendationId))
                    updateMetric(avgCoPaper[num], instituteId, coCount(institutePapers, instituteId, recommendationId))
                    updateMetric(avgCoFieldCount[num], instituteId,
                                 minSum(instituteFieldsCount, instituteId, recommendationId))
                    updateMetric(avgCoCite[num], instituteId,
                                 coCount2(instituteCitedPapers, institutePapers, instituteId, recommendationId))

        for num in hitAt:
            avgCoAuthor[num][instituteId] /= num
            avgCoPaper[num][instituteId] /= num
            avgCoFieldCount[num][instituteId] /= num
            avgCoCite[num][instituteId] /= num

    output(logFile, ' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-papers', avgCoPaper)
    outputMetric('Average Co-fields-count', avgCoFieldCount)
    outputMetric('Average Co-cites', avgCoCite)
    output(logFile)


def venueRecommendationAnalyzer():
    def venueProperties(recommendationId, venueId):
        if recommendationId == venueId:
            properties = [
                ('Authors', getLength(venueAuthors, venueId)),
                ('Fields', getLength(venueFieldsCount, venueId)),
                ('Cite & Cited by', getLength(venueCitedPapers, venueId))
            ]
        else:
            properties = [
                ('Co-authors', coCount(venueAuthors, venueId, recommendationId)),
                ('Co-fields-count', minSum(venueFieldsCount, venueId, recommendationId)),
                ('Co-cites', coCount2(venueCitedPapers, venuePapers, venueId, recommendationId))
            ]
        return '\t'.join([properties[i][0] + ': ' + str(properties[i][1]) for i in range(len(properties))])

    filePath = recommendationDir + 'venue' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    analyzedFilePath = recommendationDir + '/analyzed/venue' + filenameSuffix
    f = open(analyzedFilePath, 'w')

    venueRecommendation = dict()
    venueIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            venueId = s[i - 1].split()[1]
            venueIdSorted.append(venueId)

            f.write(s[i - 1] + '\n')
            f.write(venueProperties(venueId, venueId) + '\n')
            f.write('-' * 50 + '\n')

            venueRecommendation[venueId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 4:
                    continue
                recommendationId = splited[0]
                venueRecommendation[venueId].append(recommendationId)

                f.write(s[i + j + 1] + '\n')
                f.write(venueProperties(recommendationId, venueId) + '\n')

            f.write('\n')

    f.close()

    avgCoAuthor = dict()
    avgCoFieldCount = dict()
    avgCoCite = dict()
    for num in hitAt:
        avgCoAuthor[num] = dict()
        avgCoFieldCount[num] = dict()
        avgCoCite[num] = dict()
    for venueId in venueIdSorted:
        recommendationList = venueRecommendation[venueId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoAuthor[num], venueId, coCount(venueAuthors, venueId, recommendationId))
                    updateMetric(avgCoFieldCount[num], venueId, minSum(venueFieldsCount, venueId, recommendationId))
                    updateMetric(avgCoCite[num], venueId,
                                 coCount2(venueCitedPapers, venuePapers, venueId, recommendationId))

        for num in hitAt:
            avgCoAuthor[num][venueId] /= num
            avgCoFieldCount[num][venueId] /= num
            avgCoCite[num][venueId] /= num

    output(logFile, ' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        output(logFile, valueString, end=' ' * (12 - len(valueString)))
    output(logFile)
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-fields-count', avgCoFieldCount)
    outputMetric('Average Co-cites', avgCoCite)
    output(logFile)


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--pca', type=bool, required=False)
parser.add_argument('--norm', type=int, required=False)
parser.add_argument('--count', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--unlimited', type=bool, required=False)
parser.add_argument('--nolog', type=bool, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order
pca = parsedArgs.pca if parsedArgs.pca else False
norm = parsedArgs.norm if parsedArgs.norm else (2 if pca else 1)
count = parsedArgs.count if parsedArgs.count else 10
target = parsedArgs.target.lower().split(',') if parsedArgs.target else None
unlimited = parsedArgs.unlimited if parsedArgs.unlimited else False
noLog = parsedArgs.nolog if parsedArgs.nolog else False

recommendationDir = parentDir + '/res/%s/%s/%i/recommendation/' % (database, method, order)
filenameSuffix = 'Recommendation_norm=%i%s%s.txt' % (norm, '_PCA' if pca else '', '_unlimited' if unlimited else '')

paperYears = dict()
paperCitations = dict()
paperCitedPapers = dict()
paperFields = dict()
paperAuthors = dict()
paperVenues = dict()
paperInstitutes = dict()

authorPapers = dict()
authorInstitutes = dict()
authorYears = dict()
authorVenues = dict()
authorFieldsCount = dict()
authorCitedPapers = dict()

fieldPapers = dict()
fieldAuthors = dict()
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
venueName = dict()

infoLoader()

mkdir(['res', database, method, order, 'recommendation', 'analyzed'])

print('%s_%i%s%s' % (method, order, '_PCA' if pca else '', '_unlimited' if unlimited else ''))
print('-' * 50)

types = ['paper', 'author', 'field', 'institute', 'venue']

if noLog:
    logFile = None
else:
    logFile = open(recommendationDir + 'analyzed/recommendation_analysis.log', 'w')

for type in types:
    if target is None or type in target:
        output(logFile, type.capitalize())
        exec('%sRecommendationAnalyzer()' % type)

if not logFile is None:
    logFile.close()
