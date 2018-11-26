from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA

import numpy as np

import argparse
import os


def toHex(value):
    hexValue = str(hex(round(value * 255)))[2:].upper()
    return '0' * (2 - len(hexValue)) + hexValue


def toHexColor(color):
    return '#%s%s%s' % (toHex(color[0]), toHex(color[1]), toHex(color[2]))


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

method = parsedArgs.method if parsedArgs.method else 'WTransH_test'
order = parsedArgs.order if parsedArgs.order else 1
target = parsedArgs.target if parsedArgs.target else 'venue'
alg = parsedArgs.alg.lower() if parsedArgs.alg else 'tsne'
overwrite = parsedArgs.overwrite if parsedArgs.overwrite else False

model = method.split('_')[0].lower()

f = open('../../res/ACE17K/%s/%i/venueVector.data' % (method, order), 'r')
s = f.read().split('\n')
f.close()

nodes = []
for line in s:
    splited = line.split()
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

miscs = []
color = []
for line in s:
    splited = line.split()
    if len(splited) == 4:
        miscs.append(splited)
        color.append(toHexColor(list(map(lambda x: float(x), splited[1:]))))

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

distance = np.zeros((num, num))
for i in range(num):
    for j in range(num):
        distance[i][j] = calc(nodes[i], nodes[j], norm)
        if distance[i][j] < 0:
            distance[i][j] = 0

if alg == 'tsne':
    tsne = TSNE(n_components=2, metric='precomputed', n_iter=10000, learning_rate=150.0, perplexity=30)
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

outputName = '%s_%s' % (model, alg)
if (not overwrite) and os.path.exists('./data/%s_venue.data' % outputName):
    outputName = '%s_%s2' % (model, alg)
f = open('./data/%s_venue.data' % outputName, 'w')
for i in range(len(result)):
    vector = list(result[i])
    f.write('%f\t%f\t%s' % (vector[0], vector[1], '\t'.join(miscs[i])) + '\n')
f.close()

os.system('python canvas_painter.py --method=%s' % outputName)
