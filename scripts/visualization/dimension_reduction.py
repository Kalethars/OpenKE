from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA

import numpy as np

import argparse
import os
import time

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


def startTiming(total):
    global times, timesTotal, startTime

    times = 0
    startTime = time.time()
    timesTotal = int(total)

    print('Total loops: %i' % timesTotal)


def displayTiming():
    global times, timesTotal, startTime

    times += 1
    print('\r%s\t%.2fs' % (str(round(100. * times / timesTotal, 2)) + '%', time.time() - startTime), end='')
    if times == timesTotal:
        print()


def determineOutputName():
    modelOrig = method.split('_')[0]
    outputName = '%s_%s_%s.data' % (modelOrig, alg, target)
    n = 1
    while True:
        if (not overwrite) and os.path.exists('./data/%s' % outputName):
            n += 1
            outputName = '%s_%s%i_%s.data' % (modelOrig, alg, n, target)
        else:
            break
    print('Output file name will be: %s' % outputName)
    return outputName


def calcDistance(v1, v2, norm=1):
    return sum([abs(v1[i] - v2[i]) ** norm for i in range(len(v1))])


def calcCosSimilarity(v1, v2, norm=None):
    return 1 - sum([v1[i] * v2[i] for i in range(len(v1))])


def calcCosSimilarityForComplex(v1, v2, norm=None):
    return 1 - sum([(v1[i] * v2[i].conjugate()).real for i in range(len(v1))])


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--alg', type=str, required=False)
parser.add_argument('--overwrite', type=bool, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WComplEx_advanced'
order = parsedArgs.order if parsedArgs.order else 6
target = parsedArgs.target.lower() if parsedArgs.target else 'venue'
if not target.lower() in {'venue', 'paper'}:
    raise ValueError('Target type not supported!')
alg = parsedArgs.alg.lower() if parsedArgs.alg else 'tsne'
overwrite = parsedArgs.overwrite if parsedArgs.overwrite else False

model = method.split('_')[0].lower()

outputName = determineOutputName()

f = open('../../data/ACE17K/info/%sInfo.data' % target, 'r')
infoLines = f.read().split('\n')
f.close()

f = open('../../res/ACE17K/%s/%i/%sVector.data' % (method, order, target), 'r')
vectorLines = f.read().split('\n')
f.close()

miscs = []  # id, label, category
nodes = []
for i in range(len(infoLines)):
    splited = infoLines[i].split('\t')
    if target == 'venue':
        if len(splited) != 5:
            continue
        miscs.append([])
        miscs[-1].append(splited[0])
        miscs[-1].append(splited[2])
        miscs[-1].append(splited[3])
    else:
        if len(splited) != 2:
            continue
        miscs.append([])
        miscs[-1].append(splited[0])
        miscs[-1].append(splited[1])

    splited = vectorLines[i].split()
    if len(splited) < 2:
        continue
    if not 'complex' in model:
        nodes.append(list(map(lambda x: float(x), splited)))
    else:
        nodes.append(list(map(lambda x: complex(x), splited)))

num = len(nodes)
dimension = len(nodes[0])

f = open('./data/venue_color.data', 'r')
s = f.read().split('\n')
f.close()

color = dict()
for line in s:
    splited = line.split()
    if len(splited) == 4:
        color[splited[0]] = splited[1:]

if target == 'paper':
    f = open('../../data/ACE17K/info/venueInfo.data', 'r')
    s = f.read().split('\n')
    f.close()

    venueName = dict()
    venueCategory = dict()
    for line in s:
        splited = line.split('\t')
        if len(splited) != 5:
            continue
        venueName[splited[0]] = splited[2]
        venueCategory[splited[0]] = splited[3]

    f = open('../../benchmarks/ACE17K/triplets.txt', 'r')
    s = f.read().split('\n')
    f.close()

    paperVenue = dict()
    for line in s:
        splited = line.split()
        if len(splited) != 3:
            continue
        if splited[1] != '4':
            continue
        paperId = splited[0][1:]
        venueId = splited[2][1:]
        if not paperId in paperVenue:
            paperVenue[paperId] = dict()
        paperVenue[paperId][venueId] = paperVenue[paperId].get(venueId, 0) + 1

    for i in range(len(miscs)):
        paperId = miscs[i][0]
        if not paperId in paperVenue:
            miscs[i].append(None)
            continue
        venueId = sorted(paperVenue[paperId].keys(), key=lambda x: paperVenue[paperId][x], reverse=True)[0]
        miscs[i][1] = venueName[venueId]
        miscs[i].append(venueCategory[venueId])

norm = 1
if 'trans' in model:
    calc = calcDistance
    if model == 'wtranse2':
        norm = 2
elif 'distmult' in model:
    calc = calcCosSimilarity
elif 'complex' in model:
    calc = calcCosSimilarityForComplex
else:
    calc = calcDistance

total = num * (num + 1) / 2
startTiming(total)

distance = np.zeros((num, num))
for i in range(num):
    for j in range(i, num):
        distance[i][j] = calc(nodes[i], nodes[j], norm)
        if distance[i][j] < 0:
            distance[i][j] = 0
        distance[j][i] = distance[i][j]

        displayTiming()

if alg == 'tsne':
    tsne = TSNE(n_components=2, metric='precomputed', n_iter=10000, learning_rate=150.0, perplexity=30, verbose=True)
    tsne.fit_transform(distance)
    result = list(tsne.embedding_)
elif alg == 'lda':
    lda = LinearDiscriminantAnalysis(n_components=2)
    lda.fit(nodes, color)
    result = list(lda.transform(nodes))
elif alg == 'pca':
    pca = PCA(n_components=2)
    pca.fit_transform(nodes)
    result = list(pca.transform(nodes))
else:
    raise ValueError('Incorrect algorithm!')

f = open('./data/%s' % outputName, 'w')
for i in range(len(result)):
    if miscs[i][2] is None:
        continue
    vector = list(result[i])
    f.write('%f\t%f\t%s' % (vector[0], vector[1], '\t'.join([miscs[i][1]] + color[miscs[i][2]])) + '\n')
f.close()

os.system('python canvas_painter.py --method=%s --target=%s' %
          ('_'.join(outputName.split('_')[:2]), target))
