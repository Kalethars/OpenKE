import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def generate(dataset):
    f = open('../config/TransE.config', 'w')

    globalParams = {'threads': 32, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for epoch in [5000, 2500, 1500]:
        for nbatches in [100]:
            for alpha in [0.001]:
                for margin in [2]:
                    for bern in [0]:
                        for dimension in [1000, 500, 250]:
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
            'CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=' +
            str(i + 1) + '\n')
    f.close()


def generateDetailed(dataset):
    f = open('../config/TransE_detailed.config', 'w')

    globalParams = {'threads': 4, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

    count = 0
    for epoch in [5000]:
        for nbatches in [100]:
            for alpha in [0.0005, 0.001, 0.002, 0.01]:
                for margin in [1, 2, 3, 4]:
                    for bern in [0]:
                        for dimension in [250]:
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

    f = open('../bash/TransE_detailed.sh', 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=' +
            str(i + 1) + '\n')
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--detailed', type=int, required=False)
parsedConfig = parser.parse_args()
if parsedConfig.detailed != 1:
    generate(parsedConfig.dataset)  # Test epoch & dimension
else:
    generateDetailed(parsedConfig.dataset)  # Test alpha & margin
