import argparse


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def buildCuda(cuda):
    return ','.join(list(map(lambda x: str(x), cuda)))


def generate(method, target, config):
    configName = '%s_%s' % (method, target)
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
            'CUDA_VISIBLE_DEVICES="%s" python ../kg_train.py --method=%s --config=../config/%s.config --order=%i\n' %
            (buildCuda(config['cuda']), method, configName, i + 1))
    f.write('python ../processor/result_analyzer.py --method=%s\n' % configName)
    f.write('python ../processor/result_recommendation.py --method=%s --unlimited=True\n' % configName)
    f.write('python ../processor/recommendation_analyzer --method=%s --unlimited=True\n' % configName)
    f.write('CUDA_VISIBLE_DEVICES="%s" python ../kg_test.py --method=%s --weighted=True' %
            (buildCuda(config['cuda']), configName))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--threads', type=int, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method
target = (parsedConfig.target if parsedConfig.target else 'all').lower()
threads = parsedConfig.threads if parsedConfig.threads else 32

paramConfig = dict()
paramConfig['WTransE'] = {'basic': {'epoch': [100],
                                    'dimension': [50, 100],
                                    'nbatches': [100],
                                    'margin': [3.0],
                                    'alpha': [0.003],
                                    'bern': [0],
                                    'cuda': [1],
                                    'weighted': [False]
                                    },
                          'test': {'epoch': [5000],
                                   'dimension': [300],
                                   'nbatches': [100],
                                   'margin': [3.0],
                                   'alpha': [0.003],
                                   'bern': [0],
                                   'cuda': [1],
                                   'weighted': [False]
                                   }
                          }
paramConfig['TransE'] = {'basic': {'epoch': [2000, 1000],
                                   'dimension': [300, 200, 100],
                                   'nbatches': [100],
                                   'margin': [3.0, 2.0, 1.0],
                                   'alpha': [0.001, 0.003, 0.01],
                                   'bern': [0, 1],
                                   'cuda': [1],
                                   'weighted': [False]
                                   },
                         'advanced': {'epoch': [5000, 3500, 2000],
                                      'dimension': [300, 250, 200],
                                      'nbatches': [100],
                                      'margin': [3.0],
                                      'alpha': [0.003],
                                      'bern': [0],
                                      'cuda': [1],
                                      'weighted': [False]
                                      },
                         'detailed': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [2.0, 2.5, 3.0, 3.5],
                                      'alpha': [0.001, 0.002, 0.003, 0.004],
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
                         'weighted': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [2.5, 3.0, 3.5],
                                      'alpha': [0.002],
                                      'bern': [0],
                                      'cuda': [1],
                                      'weighted': [True]
                                      }
                         }
paramConfig['TransH'] = {'detailed': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [1.5, 2.0, 2.5, 3.0],
                                      'alpha': [0.001, 0.002, 0.003, 0.004],
                                      'bern': [0],
                                      'cuda': [1],
                                      'weighted': [False]
                                      },
                         'test': {'epoch': [5000],
                                  'dimension': [300],
                                  'nbatches': [100],
                                  'margin': [2.5],
                                  'alpha': [0.002],
                                  'bern': [0, 1],
                                  'cuda': [1],
                                  'weighted': [False]
                                  },
                         'weighted': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [2.5],
                                      'alpha': [0.002],
                                      'bern': [0],
                                      'cuda': [1],
                                      'weighted': [True]
                                      }
                         }
paramConfig['DistMult'] = {'basic': {'epoch': [1000],
                                     'dimension': [100],
                                     'nbatches': [100],
                                     'margin': [1.75, 2, 2.25, 2.25],
                                     'alpha': [0.025, 0.03, 0.035, 0.04],
                                     'bern': [0, 1],
                                     'cuda': [1],
                                     'weighted': [False]
                                     },
                           'advanced': {'epoch': [5000],
                                        'dimension': [300],
                                        'nbatches': [100],
                                        'margin': [2.5],
                                        'alpha': [0.1, 0.075, 0.05, 0.025],
                                        'bern': [0, 1],
                                        'cuda': [1],
                                        'weighted': [False]
                                        },
                           'detailed': {'epoch': [5000],
                                        'dimension': [300],
                                        'nbatches': [100],
                                        'margin': [1.75],
                                        'alpha': [0.04],
                                        'bern': [0, 1],
                                        'cuda': [1],
                                        'weighted': [False, True]
                                        },
                           'test': {'epoch': [5000],
                                    'dimension': [300],
                                    'nbatches': [100],
                                    'margin': [2.5],
                                    'alpha': [0.002],
                                    'bern': [0, 1],
                                    'cuda': [2],
                                    'weighted': [True, False]
                                    }
                           }

if target == 'all':
    for target in paramConfig[method].keys():
        generate(method, target, paramConfig[method][target])
else:
    generate(method, target, paramConfig[method][target])
