baseline = [0.2064, 0.3212, 0.2777, 0.0730, 0.2442]
s = sum([x ** 2 for x in baseline])
coeff = [x / s for x in baseline]

def getScore(splited):
    score = 0
    for i in range(len(splited)):
        try:
            score += float(splited[i]) * coeff[i]
        except:
            pass
    return score


f = open('../../data/ACE17K/info/paperInfo.data', 'r')
s = f.read().split('\n')
f.close()

paperTitle = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) != 2:
        continue
    paperTitle[splited[0]] = splited[1]

f = open('../../data/ACE17K/paperYears.data', 'r')
s = f.read().split('\n')
f.close()

paperYear = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    paperYear[splited[0]] = int(splited[1])

f = open('../../data/ACE17K/paperCitations.data', 'r')
s = f.read().split('\n')
f.close()

paperCitation = dict()
for line in s:
    splited = line.split()
    if len(splited) != 2:
        continue
    paperCitation[splited[0]] = int(splited[1])

f = open('../../benchmarks/ACE17K/triplets.txt', 'r')
s = f.read().split('\n')
f.close()

paperFields = dict()
for line in s:
    splited = line.split()
    if len(splited) != 3:
        continue
    if splited[0][0] == 'p' and splited[2][0] == 'f':
        if splited[0][1:] not in paperFields:
            paperFields[splited[0][1:]] = set()
        paperFields[splited[0][1:]].add(splited[2][1:])

method = 'WTransH_test'
order = 1
analyzedLog = '../../res/ACE17K/%s/%i/recommendation/analyzed/recommendation_paperIsInField_tail_analyzed.txt' \
              % (method, order)
f = open(analyzedLog, 'r')
s = f.read().split('\n')
f.close()

total = dict()
for i in range(len(s)):
    line = s[i]
    if '-' * 50 in line:
        paperId = s[i - 2].split()[1]
        total[paperId] = dict()
        for j in range(10):
            recommendId = s[i + 2 * j + 1].split()[1]
            splited = s[i + 2 * j + 2].split()
            total[paperId][j + 1] = total[paperId].get(j, 0) + getScore(splited)

avgAtN = 1
# papers = sorted(paperTitle.keys(), key=lambda x: total.get(x, dict()).get(avgAtN, 0))
papers = sorted(paperTitle.keys(), key=lambda x: paperCitation[x])
count = 0
for paper in papers:
    if paper not in paperFields:
        print('\t'.join([paper, 'Year: %s' % paperYear[paper], 'Cite: %s' % paperCitation[paper],
                         'Total: %s' % round(total[paper][avgAtN], 2), paperTitle[paper]]))
        count += 1
print(count)