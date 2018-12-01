import tensorflow as tf
import numpy as np
import json
import os
import time
import gc

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Params ---------------------------------------------------------------------------------------------------------------
method = 'TransE_detailed'
order = 6
epoch = 5000
alpha = 0.002
margin = 2.5


# Functions ------------------------------------------------------------------------------------------------------------

def mkdir(folders):
    path = parentDir + '/'
    for i in range(len(folders)):
        path += str(folders[i]) + '/'
        if not os.path.exists(path):
            os.mkdir(path)


def getTrainBatch(nbatches=100):
    length = int(total / nbatches)
    all = [i for i in range(total)]
    np.random.shuffle(all)
    selected = all[:length]
    positiveHeads = [trainHeadIndex[i] for i in selected]
    positiveTails = [trainTailIndex[i] for i in selected]
    positiveRelations = [trainRelationIndex[i] for i in selected]
    negativeHeads = []
    negativeTails = []
    negativeRelations = []
    for i in range(length):
        negativeRelations.append(positiveRelations[i])
        random = np.random.randint(0, 2)  # 0 for head corruption, 1 for tail corruption
        if random == 0:
            negativeTails.append(positiveTails[i])
            while True:
                randomHead = np.random.choice(allHeadsList[negativeRelations[i]])
                if buildTriplet(randomHead, negativeRelations[i], negativeTails[i]) not in triplets:
                    negativeHeads.append(randomHead)
                    break
        else:
            negativeHeads.append(positiveHeads[i])
            while True:
                randomTail = np.random.choice(allTailsList[negativeRelations[i]])
                if buildTriplet(negativeHeads[i], negativeRelations[i], randomTail) not in triplets:
                    negativeTails.append(randomTail)
                    break
    return positiveHeads, positiveRelations, positiveTails, negativeHeads, negativeRelations, negativeTails


def buildTriplet(h, r, t, reversed=False):
    h = str(h)
    r = str(r)
    t = str(t)
    if reversed:
        return ' '.join([t, r, h])
    else:
        return ' '.join([h, r, t])


def updateMetric(metric, entityId, value):
    metric[entityId] = metric.get(entityId, 0) + value


def calc(h, r, t):
    return np.sum(np.abs(h + r - t))


# Loading --------------------------------------------------------------------------------------------------------------

f = open(parentDir + '/res/ACE17K/%s/%i/embedding.vec.json' % (method, order), 'r')
data = json.load(f)
f.close()

entityResults = data['ent_embeddings']
entityVectors = tf.cast(data['ent_embeddings'], tf.float32)
dimension = entityVectors.get_shape().as_list()[1]
total = entityVectors.get_shape().as_list()[0]
print('Dimension: %i\tTotal: %i' % (dimension, total))

del data
gc.collect()

f = open(parentDir + '/benchmarks/ACE17K_new_relation/train2id.txt', 'r')
s = f.read().split('\n')
f.close()

trainHeadIndex = []
trainTailIndex = []
trainRelationIndex = []
for line in s:
    splited = line.split()
    if len(splited) == 3:
        trainHeadIndex.append(int(splited[0]))
        trainTailIndex.append(int(splited[1]))
        trainRelationIndex.append(int(splited[2]))

f = open(parentDir + '/benchmarks/ACE17K_new_relation/test2id.txt', 'r')
s = f.read().split('\n')
f.close()

testHeadIndex = []
testTailIndex = []
testRelationIndex = []
for line in s:
    splited = line.split()
    if len(splited) == 3:
        testHeadIndex.append(int(splited[0]))
        testTailIndex.append(int(splited[1]))
        testRelationIndex.append(int(splited[2]))

allHeads = dict()
allTails = dict()
allHeadsList = dict()
allTailsList = dict()
allRelations = set(trainRelationIndex) | set(testRelationIndex)
for relation in allRelations:
    allHeads[relation] = set([trainHeadIndex[i] for i in range(len(trainHeadIndex))
                              if trainRelationIndex[i] == relation]) | \
                         set([testHeadIndex[i] for i in range(len(testHeadIndex))
                              if testRelationIndex[i] == relation])
    allTails[relation] = set([trainTailIndex[i] for i in range(len(trainTailIndex))
                              if trainRelationIndex[i] == relation]) | \
                         set([testTailIndex[i] for i in range(len(testTailIndex))
                              if testRelationIndex[i] == relation])
    allHeadsList[relation] = list(allHeads[relation])
    allTailsList[relation] = list(allTails[relation])

triplets = set()
for i in range(len(trainHeadIndex)):
    triplets.add(buildTriplet(trainHeadIndex[i], trainRelationIndex[i], trainTailIndex[i]))
for i in range(len(testHeadIndex)):
    triplets.add(buildTriplet(testHeadIndex[i], testRelationIndex[i], testTailIndex[i]))

# Train ----------------------------------------------------------------------------------------------------------------

relationVectors = tf.get_variable(name="rel_embeddings", shape=[2, dimension],
                                  initializer=tf.contrib.layers.xavier_initializer(uniform=False))

hPos = tf.placeholder(tf.int64, [None])
rPos = tf.placeholder(tf.int64, [None])
tPos = tf.placeholder(tf.int64, [None])

hNeg = tf.placeholder(tf.int64, [None])
rNeg = tf.placeholder(tf.int64, [None])
tNeg = tf.placeholder(tf.int64, [None])

h = tf.nn.embedding_lookup(entityVectors, hPos)
r = tf.nn.embedding_lookup(relationVectors, rPos)
t = tf.nn.embedding_lookup(entityVectors, tPos)

h2 = tf.nn.embedding_lookup(entityVectors, hNeg)
r2 = tf.nn.embedding_lookup(relationVectors, rNeg)
t2 = tf.nn.embedding_lookup(entityVectors, tNeg)

scorePos = tf.abs(h + r - t)
scoreNeg = tf.abs(h2 + r2 - t2)

loss = tf.reduce_sum(tf.reduce_mean(scorePos - scoreNeg + margin, 1, keep_dims=False))
tf.Print(loss, [loss])
train_step = tf.train.GradientDescentOptimizer(alpha).minimize(loss)

sess = tf.InteractiveSession()
sess.run(tf.global_variables_initializer())

for i in range(epoch):
    print('\rIteration: %i' % (i + 1), end='')
    positiveHeads, positiveRelations, positiveTails, negativeHeads, negativeRelations, negativeTails = getTrainBatch()
    sess.run(train_step, feed_dict={hPos: positiveHeads, rPos: positiveRelations, tPos: positiveTails,
                                    hNeg: negativeHeads, rNeg: negativeRelations, tNeg: negativeTails})
print()

mkdir(['res', 'ACE17K_new_relation', method, order])
relationResults = sess.run(relationVectors)

f = open(parentDir + '/res/ACE17K_new_relation/%s/%i/predicted_results.json' % (method, order), 'w')
for i in range(len(relationResults)):
    for j in range(len(relationResults[i] - 1)):
        f.write('%f\t' % relationResults[i][j])
    f.write('%f\n' % relationResults[i][-1])
f.close()

# Test -----------------------------------------------------------------------------------------------------------------

metrics = dict()
metrics['MRR'] = dict()
metrics['Hit@10'] = dict()
metrics['Hit@3'] = dict()
metrics['Hit@1'] = dict()
relationCount = dict()
startTime = time.time()
for i in range(len(testHeadIndex)):
    headId = testHeadIndex[i]
    tailId = testTailIndex[i]
    relationId = testRelationIndex[i]
    relationVector = np.array(relationResults[relationId])

    print('Loop %i, head = %s, relation = %s, tail = %s' % (i + 1, headId, relationId, tailId))
    # Test Head
    key = str(relationId) + ' head'
    distances = []
    for head in allHeads[relationId]:
        headVector = np.array(entityResults[head])
        tailVector = np.array(entityResults[tailId])
        distances.append((head, calc(headVector, relationVector, tailVector)))
    distances.sort(key=lambda x: x[1])
    rank = 1
    for i in range(len(distances)):
        head = distances[i][0]
        if head == headId:
            updateMetric(metrics['MRR'], key, 1 / rank)
            updateMetric(metrics['Hit@10'], key, 1 if rank <= 10 else 0)
            updateMetric(metrics['Hit@3'], key, 1 if rank <= 3 else 0)
            updateMetric(metrics['Hit@1'], key, 1 if rank <= 1 else 0)
            updateMetric(relationCount, key, 1)
            break
        elif buildTriplet(head, relationId, tailId) not in triplets:
            rank += 1
    print('\tHead rank = %i, MRR = %f, Hit@10 = %f, Hit@3 = %f, Hit@1 = %f' %
          (rank, metrics['MRR'][key] / relationCount[key], metrics['Hit@10'][key] / relationCount[key],
           metrics['Hit@3'][key] / relationCount[key], metrics['Hit@1'][key] / relationCount[key]))
    # Test tail
    key = str(relationId) + ' tail'
    distances = []
    for tail in allTails[relationId]:
        headVector = np.array(entityResults[headId])
        tailVector = np.array(entityResults[tail])
        distances.append((tail, calc(headVector, relationVector, tailVector)))
    distances.sort(key=lambda x: x[1])
    rank = 1
    for i in range(len(distances)):
        tail = distances[i][0]
        if tail == tailId:
            updateMetric(metrics['MRR'], key, 1 / rank)
            updateMetric(metrics['Hit@10'], key, 1 if rank <= 10 else 0)
            updateMetric(metrics['Hit@3'], key, 1 if rank <= 3 else 0)
            updateMetric(metrics['Hit@1'], key, 1 if rank <= 1 else 0)
            updateMetric(relationCount, key, 1)
            break
        elif buildTriplet(headId, relationId, tail) not in triplets:
            rank += 1
    print('\tTail rank = %i, MRR = %f, Hit@10 = %f, Hit@3 = %f, Hit@1 = %f' %
          (rank, metrics['MRR'][key] / relationCount[key], metrics['Hit@10'][key] / relationCount[key],
           metrics['Hit@3'][key] / relationCount[key], metrics['Hit@1'][key] / relationCount[key]))
    print('\tTime used: %fs' % (time.time() - startTime))

for metric in metrics.keys():
    for key in metrics[metric].keys():
        metrics[metric][key] /= relationCount[key]

for key in sorted(metrics['MRR'].keys()):
    print(key, end='\t')
    for metric in ['MRR', 'Hit@10', 'Hit@3', 'Hit@1']:
        print('%s: %f' % (metric, metrics[metric][key]), end='\t')
    print(
        'Score: %f' % (metrics['MRR'][key] * (metrics['Hit@10'][key] + metrics['Hit@3'][key] + metrics['Hit@1'][key])))
