import argparse
import os

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=str, required=True)
parser.add_argument('--mode', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
methods = list(map(lambda x: x.strip(), parsedArgs.method.split(',')))
orders = list(map(lambda x: x.strip(), parsedArgs.order.split(',')))
mode = parsedArgs.mode if parsedArgs.mode else 1

if len(methods) != len(orders):
    raise ValueError('Input error!')

translationMap = {'Average Co-papers:': ('论文', {1}, max),
                  'Average Co-authors:': ('学者', {1}, max),
                  'Average Co-fields:': ('领域', {1}, max),
                  'Average Co-institutes:': ('机构', {1}, max),
                  'Average Co-venues:': ('期刊/会议', {1}, max),
                  'Average Co-cites:': ('引用/参考', {1}, max),
                  'Average Co-fields-count:': ('领域论文', {1, 2}, max),
                  'Average Co-category:': ('CCF分类', {1}, max),
                  'Average Year Diff:': ('年份差值', {2}, max),
                  'Average Year Diff Abs:': ('绝对年份差值', {2}, min),
                  'Average Citation Diff:': ('引用量差值', {2}, max),
                  'Paper': ('论文', {0}),
                  'Author': ('学者', {0}),
                  'Field': ('领域', {0}),
                  'Institute': ('机构', {0}),
                  'Venue': ('期刊/会议', {0})
                  }

results = [[] for i in range(len(methods))]
counts = dict()
count = dict()
entityType = None
for i in range(len(methods)):
    method = methods[i]
    order = orders[i]

    analysisLogPath = parentDir + \
                      '/res/%s/%s/%s/recommendation/analyzed/recommendation_analysis.log' % (database, method, order)
    f = open(analysisLogPath, 'r')
    s = f.read().split('\n')
    f.close()

    for line in s:
        splited = line.split()
        if len(splited) < 4:
            if len(splited) == 1:
                if not entityType is None:
                    counts[entityType[0]] = count
                count = dict()
                entityType = translationMap[splited[0]]
                results[i].append([entityType])
            continue
        metric = translationMap[' '.join(splited[:-3])]
        results[i].append([metric, splited[-3:]])
        for flag in metric[1]:
            count[flag] = count.get(flag, 0) + 1
counts[entityType[0]] = count

entityType = ''
for i in range(len(results[0])):
    metric = results[0][i][0]
    if len(results[0][i]) == 1:
        entityType = metric[0]
    elif mode in metric[1]:
        if entityType != '':
            print('\\midrule')
            line = '\multirow{%i}{*}{%s} ' % (counts[entityType][mode], entityType)
            entityType = ''
        else:
            line = ''
        line += '& ' + metric[0]

        func = metric[2]
        bestValue = [func([float(results[j][i][1][k]) for j in range(len(results))]) for k in range(3)]
        for j in range(len(results)):
            for k in range(3):
                line += ' & '
                if float(results[j][i][1][k]) == bestValue[k]:
                    line += '\\textbf{%s}' % results[j][i][1][k]
                else:
                    line += results[j][i][1][k]
        line += ' \\\\'
        print(line)
