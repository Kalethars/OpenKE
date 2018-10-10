import argparse


def buildString(params):
    s = ''
    for (key, value) in params.items():
        s += str(key) + '=' + str(value) + '\t'
    return s + '\n'


def generate(dataset):
    f = open('../config/TransE.config', 'w')

    globalParams = {'threads': 32, 'start': 1, 'count': 256, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

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

    f.close()


def generateStandalone(dataset):
    f = open('../config/TransE_standalone.config', 'w')

    globalParams = {'threads': 4, 'start': 1, 'count': 8, 'dataset': 'ACE17K' if dataset is None else dataset}
    f.write(buildString(globalParams))

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

    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=int, required=False)
parser.add_argument('--standalone', type=int, required=False)
parsedConfig = parser.parse_args()
if parsedConfig.standalone != 1:
    generate(parsedConfig.dataset)
else:
    generateStandalone(parsedConfig.dataset)
