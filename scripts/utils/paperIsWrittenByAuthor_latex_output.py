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


candidates = [('TransE_detailed', 6, 'TransE', 'TransE'),
              ('WTransE_test', 1, 'TransE', 'W-TransE'),
              ('TransH_test', 1, 'TransH', 'TransH'),
              ('WTransH_test', 1, 'TransH', 'W-TransH')
              ]
bestFunc = {'Average Year Diff Abs:': min,
            'Average Co-fields:': max,
            'Average Co-authors:': max,
            'Average Co-venues:': max,
            'Average Co-institutes:': max,
            'Average Co-cites:': max
            }
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

score = dict()
bestScore = dict()
outputTitle = [('Recommend papers for author:', '\\tabincell{c}{学者 \\\\ $\\downarrow$ \\\\ 论文}', -15),
               ('Recommend authors for paper:', '\\tabincell{c}{论文 \\\\ $\\downarrow$ \\\\ 学者}', -14)]
for candidate in candidates:
    method = candidate[0]
    model = candidate[2]
    name = candidate[3]

    linkPredictionLog = '../../log/ACE17K/analyzed/%s_analyzed.log' % method
    f = codecs.open(linkPredictionLog, 'r', 'utf-8')
    s = f.read().split('\n')
    f.close()

    for i in range(len(outputTitle)):
        title = outputTitle[i][0]
        lineNum = outputTitle[i][2]
        scoreValue = float(s[lineNum].split()[-2])

        if title not in score:
            score[title] = dict()
        if title not in bestScore:
            bestScore[title] = dict()

        score[title][name] = scoreValue
        if model not in bestScore[title]:
            bestScore[title][model] = scoreValue
        else:
            bestScore[title][model] = max(bestScore[title][model], scoreValue)

metricSeq = ['Average Year Diff Abs:',
             'Average Co-cites:',
             'Average Co-fields:',
             'Average Co-authors:',
             'Average Co-venues:',
             'Average Co-institutes:'
             ]
for i in range(len(outputTitle)):
    title = outputTitle[i][0]
    titleLatex = outputTitle[i][1]
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
            line += ' %i &' % avgAt[k]
            for l in range(len(metricSeq)):
                metric = metricSeq[l]
                value = values[title][name][metric][k]
                bestValue = bestValues[model][title][metric][k]
                if value == bestValue:
                    line += ' \\textbf{%s} &' % formattedRound(value, 4)
                else:
                    line += ' %s &' % formattedRound(value, 4)
            if k == 0:
                if score[title][name] == bestScore[title][model]:
                    line += ' \\multirow{%i}{*}{\\textbf{%s}}' % (len(avgAt), formattedRound(score[title][name], 3))
                else:
                    line += ' \\multirow{%i}{*}{%s}' % (len(avgAt), formattedRound(score[title][name], 3))
            line += ' \\\\'
            print(line)
    if i != len(outputTitle) - 1:
        print()
