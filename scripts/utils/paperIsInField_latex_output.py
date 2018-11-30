import codecs

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


# (method, order, baseModel, alias)
candidates = [('TransE_detailed', 6, 'TransE', 'TransE'),
              ('WTransE_test', 1, 'TransE', 'W-TransE'),
              ('TransH_test', 1, 'TransH', 'TransH'),
              ('WTransH_test', 1, 'TransH', 'W-TransH')
              ]
bestFunc = {'Average Year Diff Abs:': min}
avgAt = [10, 3, 1]
values = dict()
bestValues = dict()
for candidate in candidates:
    method = candidate[0]
    order = candidate[1]
    model = candidate[2]
    name = candidate[3]
    if model not in bestValues:
        bestValues[model] = dict()

    analysisLog = '../../res/ACE17K/%s/%i/recommendation/analyzed/relation_based_recommendation_analysis.log' \
                  % (method, order)
    f = open(analysisLog, 'r')
    s = f.read().split('\n')
    f.close()

    title = ''
    for line in s:
        if 'Recommend' in line:
            title = line
            if title not in values:
                values[title] = dict()
            values[title][name] = dict()
            if title not in bestValues[model]:
                bestValues[model][title] = dict()
            continue
        splited = line.split()
        if len(splited) <= 3:
            continue
        metric = ' '.join(splited[:-3])
        value = list(map(lambda x: float(x), splited[-3:]))
        values[title][name][metric] = value
        func = bestFunc.get(metric, max)
        if metric not in bestValues[model][title]:
            bestValues[model][title][metric] = value
        else:
            bestValues[model][title][metric] = [func(bestValues[model][title][metric][i], value[i])
                                                for i in range(len(value))]

outputTitle = ['Recommend field for papers (relation completion):']
metricSeq = ['Average Paper Index:',
             'Average Author Index:',
             'Average Venue Index:',
             'Average Institute Index:',
             'Average Co-words:',
             'Average Score:'
             ]
for i in range(len(outputTitle)):
    title = outputTitle[i]
    for j in range(len(candidates)):
        candidate = candidates[j]
        model = candidate[2]
        name = candidate[3]
        print('\\midrule')
        for k in range(len(avgAt)):
            if k == 0:
                line = '\\multirow{%i}{*}{%s} &' % (len(avgAt), name)
            else:
                line = '&'
            line += ' %i' % avgAt[k]
            for l in range(len(metricSeq)):
                metric = metricSeq[l]
                value = values[title][name][metric][k]
                bestValue = bestValues[model][title][metric][k]
                if value == bestValue:
                    line += ' & \\textbf{%s}' % formattedRound(value, 4)
                else:
                    line += ' & %s' % formattedRound(value, 4)
            line += ' \\\\'
            print(line)
    if i != len(outputTitle) - 1:
        print()
