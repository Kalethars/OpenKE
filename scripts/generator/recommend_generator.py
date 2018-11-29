f = open('../relation_based_recommendation.sh', 'w')

f.write('#!/usr/bin/env bash\n')
# methods = ['WTransE_test', 'TransH_test', 'WTransH_test', 'DistMult_detailed', 'ComplEx_advanced', 'WComplEx_advanced']
methods = ['WComplEx_advanced']
# orders = [1, 1, 1, 1, 2, 2]
orders = [2]

for i in range(len(methods)):
    method = methods[i]
    order = orders[i]
    for relation in range(7):
        for recommendObject in range(2):
            f.write('python kg_recommend.py --method=%s --order=%i --relation=%i --object=%i --replace=1 --count=0\n' %
                    (method, order, relation, recommendObject))
    f.write('cd utils\n')
    f.write('python relation_distance_mapper.py --method=%s --order=%i\n' % (method, order))
    f.write('cd ..\n')
    f.write('cd processor\n')
    f.write('python relation_based_recommendation.py --method=%s --order=%i\n' % (method, order))
    f.write('cd ..\n')

f.close()
