import argparse

importance = {'bern': 0, 'nbatches': 1, 'epoch': 2, 'dimension': 3, 'margin': 4, 'alpha': 5, 'lmbda': 6, 'weighted': 7}


def buildString(params):
    s = ''
    for key in sorted(params.keys()):
        s += str(key) + '=' + str(params[key]) + '\t'
    return s[:-1] + '\n'


def buildCuda(cuda):
    return ','.join(list(map(lambda x: str(x), cuda)))


def getParams(config, ignore={'cuda'}):
    if len(config) == len(ignore):
        yield dict()
    else:
        keys = sorted(config.keys(), key=lambda x: importance.get(x, 100))
        for key in keys:
            if not key in ignore:
                configClone = config.copy()
                del configClone[key]
                for value in config[key]:
                    for params in getParams(configClone):
                        params[key] = value
                        yield params
                break


def generate(method, target, config):
    configName = '%s_%s' % (method, target)
    f = open('../new_relation_config/%s.config' % configName, 'w')

    globalParams = {'threads': threads, 'database': database}
    f.write(buildString(globalParams))

    count = 0
    for params in getParams(config):
        f.write(buildString(params))
        count += 1

    f.close()

    f = open('../new_relation_bash/%s.sh' % configName, 'w')
    f.write('#!/usr/bin/env bash\n')
    f.write('source ~/wangrj/tensorflow/bin/activate\n')
    f.write('cd ..\n')
    for i in range(count):
        f.write(
            'CUDA_VISIBLE_DEVICES="%s" python kg_train_new_relation.py'
            ' --method=%s --config=./new_relation_config/%s.config --order=%i\n' %
            (buildCuda(config['cuda']), method, configName, i + 1))
    f.close()


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parser.add_argument('--target', type=str, required=False)
parser.add_argument('--threads', type=int, required=False)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K_new_relation'
method = parsedConfig.method if parsedConfig.method else 'all'
target = (parsedConfig.target if parsedConfig.target else 'all').lower()
threads = parsedConfig.threads if parsedConfig.threads else 32

paramConfig = dict()
paramConfig['TransE'] = {'detailed': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [2.0, 2.5, 3.0, 3.5],
                                      'alpha': [0.001, 0.002, 0.003, 0.004],
                                      'bern': [0],
                                      'cuda': [1],
                                      'model': ['TransE_detailed/6', 'WTransE_test/1']
                                      }
                         }
paramConfig['TransH'] = {'detailed': {'epoch': [5000],
                                      'dimension': [300],
                                      'nbatches': [100],
                                      'margin': [1.5, 2.0, 2.5, 3.0],
                                      'alpha': [0.001, 0.002, 0.003, 0.004],
                                      'bern': [0],
                                      'cuda': [1],
                                      'model': ['TransH_test/1', 'WTransH_test/1']
                                      }
                         }
paramConfig['DistMult'] = {'detailed': {'epoch': [5000],
                                        'dimension': [300],
                                        'nbatches': [100],
                                        'margin': [1.75],
                                        'alpha': [0.04],
                                        'bern': [0, 1],
                                        'cuda': [1],
                                      'model': ['DistMult_detailed/1']
                                        }
                           }
paramConfig['ComplEx'] = {'advanced': {'epoch': [2000],
                                       'dimension': [150],
                                       'nbatches': [100],
                                       'margin': [2.0],
                                       'alpha': [0.03, 0.05],
                                       'lmbda': [0.001, 0.01],
                                       'bern': [0, 1],
                                       'cuda': [1],
                                      'model': ['TransE_detailed/6', 'WTransE_test/1']
                                       }
                          }

if method != 'all':
    if target == 'all':
        for target in paramConfig[method].keys():
            generate(method, target, paramConfig[method][target])
    else:
        generate(method, target, paramConfig[method][target])
else:
    for method in paramConfig.keys():
        for target in paramConfig[method].keys():
            generate(method, target, paramConfig[method][target])
