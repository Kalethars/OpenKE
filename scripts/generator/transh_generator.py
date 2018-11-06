import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def generate(dataset):
    configName = 'TransH'
    f = open('../config/%s.config' % configName, 'w')

    globalParams = {'threads': 32, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for bern in [0, 1]:
        for nbatches in [100]:
            for alpha in [0.001]:
                for margin in [2]:
                    for epoch in [1500, 1000, 500]:
                        for dimension in [500, 250, 150]:
                            f.write(buildString({
                                'epoch': epoch,
                                'nbatches': nbatches,
                                'alpha': alpha,
                                'margin': margin,
                                'bern': bern,
                                'dimension': dimension
                            }))
                            count += 1

    f.close()

    f = open('../bash/%s.sh' % configName, 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransH --config=../config/%s.config --order=%i\n' % (
                configName, i + 1))
    f.close()


def generateDetailed(dataset):
    configName = 'TransH_detailed'
    f = open('../config/%s.config' % configName, 'w')

    globalParams = {'threads': 32, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for epoch in [5000]:
        for nbatches in [100]:
            for alpha in [0.0005, 0.001, 0.002, 0.01]:
                for margin in [1, 2, 3, 4]:
                    for bern in [0]:
                        for dimension in [500]:
                            f.write(buildString({
                                'epoch': epoch,
                                'nbatches': nbatches,
                                'alpha': alpha,
                                'margin': margin,
                                'bern': bern,
                                'dimension': dimension
                            }))
                            count += 1

    f.close()

    f = open('../bash/%s.sh' % configName, 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransH --config=../config/%s.config --order=%i\n' % (
                configName, i + 1))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--detailed', type=bool, required=False)
parser.add_argument('--weighted', type=bool, required=False)
parsedConfig = parser.parse_args()

detailed = parsedConfig.detailed if parsedConfig.detailed else False
weighted = parsedConfig.weighted if parsedConfig.weighted else False

if not detailed:
    generate(parsedConfig.dataset)  # Test epoch & dimension
else:
    generateDetailed(parsedConfig.dataset)  # Test alpha & margin
