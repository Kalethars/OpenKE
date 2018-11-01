import os

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

f = open(parentDir + '/data/ACE17K/PaperAuthorAffiliations.data', 'r')
s = f.read().split('\n')
f.close()

authorPapers = dict()
for line in s:
    splited = line.split()
    if len(splited) != 4:
        continue
    if authorPapers.get(splited[1], 0) == 0:
        authorPapers[splited[1]] = []
    authorPapers[splited[1]].append(splited[0])

f = open(parentDir + '/data/ACE17K/info/paperInfo.data', 'r')
s = f.read().split('\n')
f.close()

paperTitle = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) != 2:
        continue
    paperTitle[splited[0]] = splited[1]

authorId = '7E511C5F'

for paperId in authorPapers[authorId]:
    print(paperId + '\t' + paperTitle[paperId])
