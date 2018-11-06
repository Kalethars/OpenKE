import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def generate(methodKey, config):
    configName = 'TransE_' + methodKey
    f = open('../config/%s.config' % configName, 'w')

    globalParams = {'threads': threads, 'dataset': dataset}
    f.write(buildString(globalParams))

    count = 0
    for nbatches in config['nbatches']:
        for bern in config['bern']:
            for alpha in config['alpha']:
                for margin in config['margin']:
                    for epoch in config['epoch']:
                        for dimension in config['dimension']:
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
            'CUDA_VISIBLE_DEVICES="%s" python ../kg_train.py --method=TransE --config=../config/%s.config --order=%i\n' % (
                cuda, configName, i + 1))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--dataset', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--threads', type=int, required=False)
parser.add_argument('--cuda', type=str, required=False)
parsedConfig = parser.parse_args()

dataset = parsedConfig.dataset if parsedConfig.dataset else 'ACE17K'
method = (parsedConfig.method if parsedConfig.method else 'all').lower()
threads = parsedConfig.threads if parsedConfig.threads else 32
cuda = parsedConfig.cuda if parsedConfig.cuda else '1'

paramConfig = {'basic': {'epoch': [2000, 1000],
                         'dimension': [300, 200, 100],
                         'nbatches': [100, 200],
                         'margin': [3.0, 2.0, 1.0],
                         'alpha': [0.001, 0.003, 0.01],
                         'bern': [0, 1]},
               'advanced': {'epoch': [5000, 3500, 2000],
                            'dimension': [800, 500, 300],
                            'nbatches': [100],
                            'margin': [2.0],
                            'alpha': [0.001],
                            'bern': [0]},
               'detailed': {'epoch': [5000],
                            'dimension': [500],
                            'nbatches': [100],
                            'margin': [1.5, 2.0, 2.5, 3.0],
                            'alpha': [0.0005, 0.001, 0.003, 0.01],
                            'bern': [0]}
               }

if method == 'all':
    for methodKey in paramConfig.keys():
        generate(methodKey, paramConfig[methodKey])
else:
    generate(method, paramConfig[method])
