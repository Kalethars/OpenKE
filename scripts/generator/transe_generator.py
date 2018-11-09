import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def generate(methodKey, config):
    configName = 'TransE_' + methodKey
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
            'CUDA_VISIBLE_DEVICES="%s" python ../kg_train.py --method=TransE --config=../config/%s.config --order=%i\n' %
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

paramConfig = {'basic': {'epoch': [2000, 1000],
                         'dimension': [300, 200, 100],
                         'nbatches': [100],
                         'margin': [3.0, 2.0, 1.0],
                         'alpha': [0.001, 0.003, 0.01],
                         'bern': [0, 1],
                         'cuda': [1],
                         'weighted': [False]
                         },
               'advanced': {'epoch': [5000, 3500, 2000],
                            'dimension': [500, 300],
                            'nbatches': [100],
                            'margin': [3.0],
                            'alpha': [0.003],
                            'bern': [0],
                            'cuda': [1],
                            'weighted': [False]
                            },
               'detailed': {'epoch': [5000],
                            'dimension': [500],
                            'nbatches': [100],
                            'margin': [2.0, 2.5, 3.0, 3.5],
                            'alpha': [0.001, 0.003, 0.005],
                            'bern': [0],
                            'cuda': [1],
                            'weighted': [False]
                            },
               'test': {'epoch': [1000],
                        'dimension': [100],
                        'nbatches': [100],
                        'margin': [3.0],
                        'alpha': [0.003],
                        'bern': [0],
                        'cuda': [2],
                        'weighted': [True, False]
                        },
               'weighted': {'epoch': [2000],
                            'dimension': [300],
                            'nbatches': [100],
                            'margin': [3.0],
                            'alpha': [0.003],
                            'bern': [0],
                            'cuda': [1],
                            'weighted': [True, False]
                            }
               }

if method == 'all':
    for methodKey in paramConfig.keys():
        generate(methodKey, paramConfig[methodKey])
else:
    generate(method, paramConfig[method])
