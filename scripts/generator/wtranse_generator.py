import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def generate(methodKey, config):
    configName = 'WTransE_' + methodKey
    f = open('../config/%s.config' % configName, 'w')

    globalParams = {'threads': threads, 'database': database}
    f.write(buildString(globalParams))

    count = 0
    for nbatches in config['nbatches']:
        for bern in config['bern']:
            for alpha in config['alpha']:
                for margin in config['margin']:
                    for epoch in config['epoch']:
                        for dimension in config['dimension']:
                            for weighted in config['weighted']:
                                f.write(buildString({
                                    'epoch': epoch,
                                    'nbatches': nbatches,
                                    'alpha': alpha,
                                    'margin': margin,
                                    'bern': bern,
                                    'dimension': dimension,
                                    'weighted': weighted
                                }))
                                count += 1

    f.close()

    f = open('../bash/%s.sh' % configName, 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="%s" python ../kg_train.py --method=WTransE --config=../config/%s.config --order=%i\n' %
            (','.join(list(map(lambda x: str(x), config['cuda']))), configName, i + 1))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--threads', type=int, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = (parsedConfig.method if parsedConfig.method else 'all').lower()
threads = parsedConfig.threads if parsedConfig.threads else 32

paramConfig = {'test': {'epoch': [1000],
                        'dimension': [100],
                        'nbatches': [100],
                        'margin': [3.0],
                        'alpha': [0.003],
                        'bern': [0],
                        'cuda': [0],
                        'weighted': [False]
                        }
               }

if method == 'all':
    for methodKey in paramConfig.keys():
        generate(methodKey, paramConfig[methodKey])
else:
    generate(method, paramConfig[method])
