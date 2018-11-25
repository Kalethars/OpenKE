from sklearn.manifold import TSNE
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA

import argparse
import os


def toHex(value):
    hexValue = str(hex(round(value * 255)))[2:].upper()
    return '0' * (2 - len(hexValue)) + hexValue


def toHexColor(color):
    return '#%s%s%s' % (toHex(color[0]), toHex(color[1]), toHex(color[2]))


parser = argparse.ArgumentParser()
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--alg', type=str, required=False)
parsedArgs = parser.parse_args()

method = parsedArgs.method if parsedArgs.method else 'WTransH_test'
order = parsedArgs.order if parsedArgs.order else 1
target = parsedArgs.target if parsedArgs.target else 'venue'
alg = parsedArgs.alg.lower() if parsedArgs.alg else 'tsne'

f = open('../../res/ACE17K/%s/%i/venueVector.data' % (method, order), 'r')
s = f.read().split('\n')
f.close()

nodes = []
for line in s:
    splited = line.split()
    if len(splited) < 2:
        continue
    nodes.append(list(map(lambda x: float(x), splited)))

f = open('./data/%s_venue.data' % method, 'r')
s = f.read().split('\n')
f.close()

miscs = []
color = []
for line in s:
    splited = line.split()
    if len(splited) == 6:
        miscs.append(splited[2:])
        color.append(toHexColor(list(map(lambda x: float(x), splited[3:]))))

if alg == 'tsne':
    tsne = TSNE(n_components=2)
    tsne.fit_transform(nodes)
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

outputName = method.split('_')[0] + '_%s_venue.data' % alg
if os.path.exists('./data/%s' % outputName):
    outputName = method.split('_')[0] + '_%s2_venue.data' % alg
f = open('./data/%s' % outputName, 'w')
for i in range(len(result)):
    vector = list(result[i])
    f.write('%f\t%f\t%s' % (vector[0], vector[1], '\t'.join(miscs[i])) + '\n')
f.close()
