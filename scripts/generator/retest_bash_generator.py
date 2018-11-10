import argparse
import os

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parsedConfig = parser.parse_args()

database = parsedConfig.database if parsedConfig.database else 'ACE17K'
method = parsedConfig.method

resultDir = parentDir + '/res/%s/%s/' % (database, method)
fileList = os.listdir(resultDir)

testBashPath = parentDir + '/scripts/test/test_%s_%s.sh' % (database, method)
f = open(testBashPath, 'w')
f.write('#!/usr/bin/env bash\n')
f.write('source ~/wangrj/tensorflow/bin/activate\n')

for order in sorted(fileList, key=lambda x: int(x)):
    f.write('python ../kg_test.py --database=%s --method=%s --order=%s\n' % (database, method, order))

f.close()
