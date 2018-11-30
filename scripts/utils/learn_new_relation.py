from __future__ import print_function
from __future__ import division

import os
import random

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
database = 'ACE17K'


def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def addToSet(data, a, b):
    if data.get(a, 0) == 0:
        data[a] = set()
    if type(b) is set:
        data[a] = data[a] | b
    else:
        data[a].add(b)


def loadAuthorVenue():
    f = open(parentDir + '/benchmarks/%s/triplets.txt' % database, 'r')
    s = f.read().split('\n')
    f.close()

    paperAuthor = dict()
    paperVenue = dict()
    authorVenue = []
    for line in s:
        splited = line.split()
        if len(splited) == 3:
            headId = splited[0][1:]
            relationId = splited[1]
            tailId = splited[2][1:]

            if relationId == '2':
                addToSet(paperAuthor, headId, tailId)
            elif relationId == '4':
                addToSet(paperVenue, headId, tailId)

    for paperId in paperAuthor.keys():
        for authorId in paperAuthor[paperId]:
            for venueId in paperVenue.get(paperId, set()):
                authorVenue.append((entityIndex[authorId], entityIndex[venueId]))

    return authorVenue


def loadPaperInstitute():
    f = open(parentDir + '/data/%s/PaperAuthorAffiliations.data' % database, 'r')
    s = f.read().split('\n')
    f.close()

    paperInstitute = []
    for line in s:
        splited = line.split('\t')
        if len(splited) != 4:
            continue
        if len(splited[2]) != 8:
            continue
        paperId = splited[0]
        instituteId = splited[2]
        paperInstitute.append((entityIndex[paperId], entityIndex[instituteId]))

    return paperInstitute


def loadEntities():
    f = open(parentDir + '/benchmarks/%s/entity2id.txt' % database, 'r')
    s = f.read().split('\n')
    f.close()

    f = open(newDir + 'entity2id.txt', 'w')
    entityIndex = dict()
    for line in s:
        f.write(line + '\n')
        splited = line.split()
        if len(splited) != 2:
            continue
        entityIndex[splited[0][1:]] = splited[1]
    f.close()

    return entityIndex


mkdir(['benchmarks', '%s_new_relation' % database])
newDir = parentDir + '/benchmarks/%s_new_relation/' % database

f = open(newDir + 'relation2id.txt', 'w')
f.write('2\n')
f.write('author_participate_in_venue 0\n')
f.write('paper_is_produced_by_institute 1\n')
f.close()

entityIndex = loadEntities()

authorVenue = loadAuthorVenue()
paperInstitute = loadPaperInstitute()

random.shuffle(authorVenue)
random.shuffle(paperInstitute)

percentage = 0.9

authorVenueTotal = round(len(authorVenue) * percentage)
paperInstituteTotal = round(len(paperInstitute) * percentage)

f = open(newDir + 'train2id.txt', 'w')
g = open(newDir + 'train2id_weighted.txt', 'w')
f.write('%i\n' % (authorVenueTotal + paperInstituteTotal))
g.write('%i\n' % (authorVenueTotal + paperInstituteTotal))
for i in range(authorVenueTotal):
    f.write('%s %s 0\n' % (authorVenue[i][0], authorVenue[i][1]))
    g.write('%s %s 0 1.0\n' % (authorVenue[i][0], authorVenue[i][1]))
for i in range(paperInstituteTotal):
    f.write('%s %s 0\n' % (paperInstitute[i][0], paperInstitute[i][1]))
    g.write('%s %s 0 1.0\n' % (paperInstitute[i][0], paperInstitute[i][1]))
f.close()

f = open(newDir + 'test2id.txt', 'w')
g = open(newDir + 'test2id_weighted.txt', 'w')
f.write('%i\n' % (len(authorVenue) + len(paperInstitute) - authorVenueTotal - paperInstituteTotal))
g.write('%i\n' % (len(authorVenue) + len(paperInstitute) - authorVenueTotal - paperInstituteTotal))
for i in range(authorVenueTotal, len(authorVenue)):
    f.write('%s %s 0\n' % (authorVenue[i][0], authorVenue[i][1]))
    g.write('%s %s 0 1.0\n' % (authorVenue[i][0], authorVenue[i][1]))
for i in range(paperInstituteTotal, len(paperInstitute)):
    f.write('%s %s 0\n' % (paperInstitute[i][0], paperInstitute[i][1]))
    g.write('%s %s 0 1.0\n' % (paperInstitute[i][0], paperInstitute[i][1]))
f.close()
g.close()

f = open(newDir + 'valid2id.txt', 'w')
g = open(newDir + 'valid2id_weighted.txt', 'w')
f.write('0\n')
g.write('0\n')
f.close()
g.close()

authorVenueHeads = set([authorId for (authorId, venueId) in authorVenue])
authorVenueTails = set([venueId for (authorId, venueId) in authorVenue])
paperInstituteHeads = set([paperId for (paperId, instituteId) in paperInstitute])
paperInstituteTails = set([instituteId for (paperId, instituteId) in paperInstitute])

f = open(newDir + 'type_constrain.txt', 'w')
f.write('2\t%i\t%i\n' % (len(authorVenueHeads) + len(paperInstituteHeads),
                         len(authorVenueTails) + len(paperInstituteTails)))

f.write('0\t%i' % len(authorVenueHeads))
for authorId in authorVenueHeads:
    f.write('\t%s' % authorId)
f.write('\n')

f.write('0\t%i' % len(authorVenueTails))
for venueId in authorVenueTails:
    f.write('\t%s' % venueId)
f.write('\n')

f.write('1\t%i' % len(paperInstituteHeads))
for paperId in paperInstituteHeads:
    f.write('\t%s' % paperId)
f.write('\n')

f.write('1\t%i' % len(paperInstituteTails))
for instituteId in paperInstituteTails:
    f.write('\t%s' % instituteId)
f.write('\n')

f.close()
