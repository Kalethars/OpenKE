import argparse


def buildString(params):
    s = ''
    for (key, value) in params.items():
        s += str(key) + '=' + str(value) + '\t'
    return s[:-1] + '\n'


def generate(dataset):
    f = open('../config/TransE.config', 'w')

    globalParams = {'threads': 32, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for epoch in [1000, 1500]:
        for nbatches in [100, 200]:
            for alpha in [0.001, 0.01]:
                for margin in [1, 2, 3, 4]:
                    for bern in [0, 1]:
                        for dimension in [100, 150, 200, 250]:
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

    f = open('../bash/TransE.sh', 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=' +
            str(i + 1) + '\n')
    f.close()


def generateStandalone(dataset):
    f = open('../config/TransE_standalone.config', 'w')

    globalParams = {'threads': 4, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for epoch in [1000, 1500]:
        for nbatches in [200]:
            for alpha in [0.001]:
                for margin in [1, 2]:
                    for bern in [0]:
                        for dimension in [100, 200]:
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

    f = open('../bash/TransE_standalone.sh', 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=TransE --config=../config/TransE_standalone.config --order=' +
            str(i + 1) + '\n')
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--standalone', type=int, required=False)
parsedConfig = parser.parse_args()
if parsedConfig.standalone != 1:
    generate(parsedConfig.dataset)
else:
    generateStandalone(parsedConfig.dataset)
