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
    outputName = '%s_%s_%s_paper.data' % (modelOrig, alg, category)
    n = 1
    while True:
        if (not overwrite) and os.path.exists('./data/%s' % outputName):
            n += 1
            outputName = '%s_%s%i_%s_paper.data' % (modelOrig, alg, n, category)
        else:
            break
    print('Output file name will be: %s' % outputName)
    return outputName


def calcDistance(v1, v2, norm=1):
    return np.sum(np.power(np.abs(v1 - v2), norm))


def calcCosSimilarity(v1, v2, norm=None):
    return 1 - np.sum(v1 * v2)


def calcCosSimilarityForComplex(v1, v2, norm=None):
    return 1 - np.sum(np.real(v1 * np.conj(v2)))


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--alg', type=str, required=False)
parser.add_argument('--category', type=str, required=False)
parser.add_argument('--overwrite', type=bool, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WComplEx_advanced'
order = parsedArgs.order if parsedArgs.order else 6
alg = parsedArgs.alg.lower() if parsedArgs.alg else 'tsne'
category = parsedArgs.category.upper() if parsedArgs.category else 'AI'
overwrite = parsedArgs.overwrite if parsedArgs.overwrite else False

model = method.split('_')[0].lower()

f = open('./data/venue_%s_color.data' % category, 'r')
s = f.read().split('\n')
f.close()

color = dict()
for line in s:
    splited = line.split()
    if len(splited) == 4:
        color[splited[0]] = splited[1:]
legalVenues = set(color.keys())

outputName = determineOutputName()

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
    if venueName[venueId] not in legalVenues:
        continue
    if paperId not in paperVenue:
        paperVenue[paperId] = dict()
    paperVenue[paperId][venueId] = paperVenue[paperId].get(venueId, 0) + 1

for paperId in paperVenue.keys():
    if len(paperVenue[paperId]) == 0:
        paperVenue[paperId] = None
        continue
    sortedVenueId = sorted(paperVenue[paperId].items(), key=lambda x: x[1], reverse=True)
    paperVenue[paperId] = sortedVenueId[0][0]

f = open('../../data/ACE17K/info/paperInfo.data', 'r')
infoLines = f.read().split('\n')
f.close()

f = open('../../res/ACE17K/%s/%i/paperVector.data' % (method, order), 'r')
vectorLines = f.read().split('\n')
f.close()

miscs = []  # id, label
nodes = []
for i in range(len(infoLines)):
    splited = infoLines[i].split('\t')
    if len(splited) != 2:
        continue
    paperId = splited[0]
    paperName = splited[1]
    if paperVenue.get(paperId, None) is None:
        continue
    miscs.append([])
    miscs[-1].append(paperId)
    miscs[-1].append(venueName[paperVenue[paperId]])

    splited = vectorLines[i].split()
    if len(splited) < 2:
        continue
    if not 'complex' in model:
        nodes.append(np.array(list(map(lambda x: float(x), splited))))
    else:
        nodes.append(np.array(list(map(lambda x: complex(x), splited))))

num = len(nodes)
distance = np.zeros((num, num))
if alg in {'tsne'}:
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
elif alg == 'origin':
    result = nodes
else:
    raise ValueError('Incorrect algorithm!')

f = open('./data/%s' % outputName, 'w')
for i in range(len(result)):
    if miscs[i][1] is None:
        continue
    vector = list(result[i])
    f.write('%f\t%f\t%s' % (vector[0], vector[1], '\t'.join([miscs[i][1]] + color[miscs[i][1]])) + '\n')
f.close()

os.system('python canvas_painter.py --method=%s --target=paper --std=100 --dx=-50' %
          ('_'.join(outputName.split('_')[:-1])))
