import argparse
import os
import win_unicode_console

win_unicode_console.enable()

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

hitAt = [10, 3, 1]


def output(f, s='', end='\n'):
    print(s + end, end='')
    f.write(s + end)


def outputMetric(metricString, metric, digit=4):
    print(metricString + ':', end=' ' * (24 - len(metricString)))
    for num in sorted(metric.keys(), reverse=True):
        valueString = formattedRound(averageValue(metric[num].values()), digit)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def coCount(data, a, b):
    return len(data.get(a, set()) & data.get(b, set()))


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

    def loadTriplets():
        global paperCites, paperFields, paperAuthors, paperVenues
        global authorPapers, authorFields, authorInstitutes, authorYears
        global fieldPapers, fieldAuthors
        global instituteAuthors
        global venuePapers

        filePath = parentDir + '/benchmarks/%s/triplets.txt' % database
        f = open(filePath, 'r')
        s = f.read().split('\n')
        f.close()

        paperCites = dict()
        paperFields = dict()
        paperAuthors = dict()
        paperVenues = dict()

        authorPapers = dict()
        authorFields = dict()
        authorInstitutes = dict()
        authorYears = dict()
        authorYears['count'] = dict()

        fieldPapers = dict()
        fieldAuthors = dict()

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
                    addToSet(paperCites, headId, tailId)
                    addToSet(paperCites, tailId, headId)
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
                    addToSet(authorFields, headId, tailId)
                    addToSet(fieldAuthors, tailId, headId)
                if tailType == 'i':
                    addToSet(authorInstitutes, headId, tailId)
                    addToSet(instituteAuthors, tailId, headId)

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
        global authorVenues, venueAuthors, venueFieldsCount

        authorVenues = dict()
        venueAuthors = dict()
        for authorId in authorPapers.keys():
            for paperId in authorPapers[authorId]:
                for venueId in paperVenues.get(paperId, set()):
                    addToSet(authorVenues, authorId, venueId)
                    addToSet(venueAuthors, venueId, authorId)

        venueFieldsCount = dict()
        for venueId in venuePapers.keys():
            venueFieldsCount[venueId] = dict()
            for paperId in venuePapers[venueId]:
                for fieldId in paperFields.get(paperId, set()):
                    updateMetric(venueFieldsCount[venueId], fieldId, 1)

    loadPaperYears()
    loadTriplets()
    loadPaperInstitutes()
    calcSecondaryCounts()


def paperRecommendationAnalyzer():
    filePath = recommendationDir + 'paper' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    paperRecommendation = dict()
    paperIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            paperId = s[i - 1].split()[1]
            paperRecommendation[paperId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) <= 2:
                    continue
                recommendationId = splited[0]
                paperRecommendation[paperId].append(recommendationId)
            paperIdSorted.append(paperId)

    avgYearDiff = dict()
    avgYearDiffAbs = dict()
    avgCoCite = dict()
    avgCoField = dict()
    avgCoAuthor = dict()
    avgCoVenue = dict()
    avgCoInstitute = dict()
    for num in hitAt:
        avgYearDiff[num] = dict()
        avgYearDiffAbs[num] = dict()
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
                    updateMetric(avgCoCite[num], paperId, coCount(paperCites, paperId, recommendationId))
                    if recommendationId in paperCites.get(paperId, set()):
                        updateMetric(avgCoCite[num], paperId, 1)
                    updateMetric(avgCoField[num], paperId, coCount(paperFields, paperId, recommendationId))
                    updateMetric(avgCoAuthor[num], paperId, coCount(paperAuthors, paperId, recommendationId))
                    updateMetric(avgCoVenue[num], paperId, coCount(paperVenues, paperId, recommendationId))
                    updateMetric(avgCoInstitute[num], paperId, coCount(paperInstitutes, paperId, recommendationId))

        for num in hitAt:
            avgYearDiff[num][paperId] /= num
            avgYearDiffAbs[num][paperId] /= num
            avgCoCite[num][paperId] /= num
            avgCoField[num][paperId] /= num
            avgCoAuthor[num][paperId] /= num
            avgCoVenue[num][paperId] /= num
            avgCoInstitute[num][paperId] /= num

    print(' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()
    outputMetric('Average Year Diff', avgYearDiff)
    outputMetric('Average Year Diff Abs', avgYearDiffAbs)
    outputMetric('Average Co-cites', avgCoCite)
    outputMetric('Average Co-fields', avgCoField)
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-venues', avgCoVenue)
    outputMetric('Average Co-institutes', avgCoInstitute)
    print()


def authorRecommendationAnalyzer():
    filePath = recommendationDir + 'author' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    authorRecommendation = dict()
    authorIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            authorId = s[i - 1].split()[1]
            authorRecommendation[authorId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) <= 2:
                    continue
                recommendationId = splited[0]
                authorRecommendation[authorId].append(recommendationId)
            authorIdSorted.append(authorId)

    avgYearDiff = dict()
    avgYearDiffAbs = dict()
    avgCoPaper = dict()
    avgCoField = dict()
    avgCoInstitute = dict()
    avgCoVenue = dict()
    for num in hitAt:
        avgYearDiff[num] = dict()
        avgYearDiffAbs[num] = dict()
        avgCoPaper[num] = dict()
        avgCoField[num] = dict()
        avgCoInstitute[num] = dict()
        avgCoVenue[num] = dict()
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
                    updateMetric(avgCoField[num], authorId, coCount(authorFields, authorId, recommendationId))
                    updateMetric(avgCoInstitute[num], authorId, coCount(authorInstitutes, authorId, recommendationId))
                    updateMetric(avgCoVenue[num], authorId, coCount(authorVenues, authorId, recommendationId))

        for num in hitAt:
            avgYearDiff[num][authorId] /= num
            avgYearDiffAbs[num][authorId] /= num
            avgCoPaper[num][authorId] /= num
            avgCoField[num][authorId] /= num
            avgCoInstitute[num][authorId] /= num
            avgCoVenue[num][authorId] /= num

    print(' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()
    outputMetric('Average Year Diff', avgYearDiff)
    outputMetric('Average Year Diff Abs', avgYearDiffAbs)
    outputMetric('Average Co-papers', avgCoPaper)
    outputMetric('Average Co-fields', avgCoField)
    outputMetric('Average Co-institutes', avgCoInstitute)
    outputMetric('Average Co-venues', avgCoVenue)
    print()


def fieldRecommendationAnalyzer():
    filePath = recommendationDir + 'field' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    fieldRecommendation = dict()
    fieldIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            fieldId = s[i - 1].split()[1]
            fieldRecommendation[fieldId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) <= 2:
                    continue
                recommendationId = splited[0]
                fieldRecommendation[fieldId].append(recommendationId)
            fieldIdSorted.append(fieldId)

    avgCoPaper = dict()
    avgCoAuthor = dict()
    for num in hitAt:
        avgCoPaper[num] = dict()
        avgCoAuthor[num] = dict()
    for fieldId in fieldIdSorted:
        recommendationList = fieldRecommendation[fieldId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoPaper[num], fieldId, coCount(fieldPapers, fieldId, recommendationId))
                    updateMetric(avgCoAuthor[num], fieldId, coCount(fieldAuthors, fieldId, recommendationId))

        for num in hitAt:
            avgCoPaper[num][fieldId] /= num
            avgCoAuthor[num][fieldId] /= num

    print(' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()
    outputMetric('Average Co-papers', avgCoPaper)
    outputMetric('Average Co-authors', avgCoAuthor)
    print()


def instituteRecommendationAnalyzer():
    filePath = recommendationDir + 'institute' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    instituteRecommendation = dict()
    instituteIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            instituteId = s[i - 1].split()[1]
            instituteRecommendation[instituteId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) <= 2:
                    continue
                recommendationId = splited[0]
                instituteRecommendation[instituteId].append(recommendationId)
            instituteIdSorted.append(instituteId)

    avgCoAuthor = dict()
    avgCoPaper = dict()
    for num in hitAt:
        avgCoAuthor[num] = dict()
        avgCoPaper[num] = dict()
    for instituteId in instituteIdSorted:
        recommendationList = instituteRecommendation[instituteId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoAuthor[num], instituteId,
                                 coCount(instituteAuthors, instituteId, recommendationId))
                    updateMetric(avgCoPaper[num], instituteId, coCount(institutePapers, instituteId, recommendationId))

        for num in hitAt:
            avgCoAuthor[num][instituteId] /= num
            avgCoPaper[num][instituteId] /= num

    print(' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-papers', avgCoPaper)
    print()


def venueRecommendationAnalyzer():
    filePath = recommendationDir + 'venue' + filenameSuffix
    f = open(filePath, 'r')
    s = f.read().split('\n')
    f.close()

    venueRecommendation = dict()
    venueIdSorted = []
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            venueId = s[i - 1].split()[1]
            venueRecommendation[venueId] = []
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) <= 2:
                    continue
                recommendationId = splited[0]
                venueRecommendation[venueId].append(recommendationId)
            venueIdSorted.append(venueId)

    avgCoAuthor = dict()
    avgCoFieldCount = dict()
    for num in hitAt:
        avgCoAuthor[num] = dict()
        avgCoFieldCount[num] = dict()
    for venueId in venueIdSorted:
        recommendationList = venueRecommendation[venueId]
        for i in range(len(recommendationList)):
            recommendationId = recommendationList[i]
            for num in hitAt:
                if i < num:
                    updateMetric(avgCoAuthor[num], venueId, coCount(venueAuthors, venueId, recommendationId))
                    updateMetric(avgCoFieldCount[num], venueId, minSum(venueFieldsCount, venueId, recommendationId))

        for num in hitAt:
            avgCoAuthor[num][venueId] /= num
            avgCoFieldCount[num][venueId] /= num

    print(' ' * 25, end='')
    for num in hitAt:
        valueString = 'Hit@' + str(num)
        print(valueString, end=' ' * (12 - len(valueString)))
    print()
    outputMetric('Average Co-authors', avgCoAuthor)
    outputMetric('Average Co-field-counts', avgCoFieldCount)
    print()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=True)
parser.add_argument('--pca', type=bool, required=False)
parser.add_argument('--norm', type=int, required=False)
parser.add_argument('--count', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--unlimited', type=bool, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order
pca = parsedArgs.pca if parsedArgs.pca else False
norm = parsedArgs.norm if parsedArgs.norm else (2 if pca else 1)
count = parsedArgs.count if parsedArgs.count else 10
target = parsedArgs.target.lower() if parsedArgs.target else None
unlimited = parsedArgs.unlimited if parsedArgs.unlimited else False

recommendationDir = parentDir + '/res/%s/%s/%i/recommendation/' % (database, method, order)
filenameSuffix = 'Recommendation_norm=%i%s%s.txt' % (norm, '_PCA' if pca else '', '_unlimited' if unlimited else '')

paperYears = dict()
paperCites = dict()
paperFields = dict()
paperAuthors = dict()
paperVenues = dict()
paperInstitutes = dict()

authorPapers = dict()
authorFields = dict()
authorInstitutes = dict()
authorYears = dict()
authorVenues = dict()

fieldPapers = dict()
fieldAuthors = dict()

instituteAuthors = dict()
institutePapers = dict()

venuePapers = dict()
venueAuthors = dict()
venueFieldsCount = dict()

infoLoader()

print('%s_%i%s%s' % (method, order, '_PCA' if pca else '', '_unlimited' if unlimited else ''))
print('-' * 50)

types = ['paper', 'author', 'field', 'institute', 'venue']

for type in types:
    if target is None or target == type:
        print(type.capitalize())
        exec('%sRecommendationAnalyzer()' % type)
