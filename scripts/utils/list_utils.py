import os


def prepareAuthorPaper():
    if len(authorPapers) == 0:
        f = open(parentDir + '/data/ACE17K/PaperAuthorAffiliations.data', 'r')
        s = f.read().split('\n')
        f.close()

        for line in s:
            splited = line.split()
            if len(splited) != 4:
                continue
            if authorPapers.get(splited[1], 0) == 0:
                authorPapers[splited[1]] = []
            authorPapers[splited[1]].append(splited[0])

    if len(paperTitle) == 0:
        f = open(parentDir + '/data/ACE17K/info/paperInfo.data', 'r')
        s = f.read().split('\n')
        f.close()

        for line in s:
            splited = line.split('\t')
            if len(splited) != 2:
                continue
            paperTitle[splited[0]] = splited[1]


def prepareInstituteAuthor():
    if len(instituteAuthors) == 0:
        f = open(parentDir + '/data/ACE17K/PaperAuthorAffiliations.data', 'r')
        s = f.read().split('\n')
        f.close()

        for line in s:
            splited = line.split()
            if len(splited) != 4:
                continue
            if instituteAuthors.get(splited[2], 0) == 0:
                instituteAuthors[splited[2]] = set()
            instituteAuthors[splited[2]].add(splited[1])

    if len(authorName) == 0:
        f = open(parentDir + '/data/ACE17K/info/authorInfo.data', 'r')
        s = f.read().split('\n')
        f.close()

        for line in s:
            splited = line.split('\t')
            if len(splited) != 2:
                continue
            authorName[splited[0]] = splited[1]


parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

authorPapers = dict()
paperTitle = dict()
instituteAuthors = dict()
authorName = dict()

prepareAuthorPaper()
prepareInstituteAuthor()

for authorId in instituteAuthors['0AE9651A']:  # Shanghai Jiao Tong University
    print(authorId + '\t' + authorName[authorId])
    for paperId in authorPapers[authorId]:
        print('\t' + paperId + '\t' + paperTitle[paperId])
    print()
