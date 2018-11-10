import argparse
import codecs
import os
import win_unicode_console

win_unicode_console.enable()

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def output(f, s='', end='\n'):
    print(str(s) + end, end='')
    f.write(str(s) + end)


def average(list):
    return float(sum(list)) / len(list)


def buildEquation(name, value):
    return str(name) + ' = ' + str(round(value, 6))


def solveMetricMistake(metric):
    if not metricMistake:
        return metric
    if metric == 'MR':
        return 'MRR'
    elif metric == 'MRR':
        return 'MR'
    else:
        return metric


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def parameterValueToString(parameterValue, parameterName):
    if parameterName == 'alpha':
        return str(str(parameterValue).rstrip('0'))
    elif parameterName in ['bern', 'dimension', 'epoch', 'nbatches']:
        return str(round(parameterValue))
    elif parameterName == 'margin':
        return str(formattedRound(parameterValue, 1))


def calcScore(scoreResults):
    return scoreResults['MRR'] * (scoreResults['hit@10'] + scoreResults['hit@3'] + scoreResults['hit@1'])


def score(result):
    if result.get('scoreResults', 0) == 0:
        sumByMetric = dict()
        result['scoreResults'] = dict()
        for relationName in result['relationResults'].keys():
            for predictEntity in result['relationResults'][relationName].keys():
                for metric in result['relationResults'][relationName][predictEntity].keys():
                    sumByMetric[metric] = sumByMetric.get(metric, 0) + \
                                          result['relationResults'][relationName][predictEntity][metric]
        relationNumber = len(result['relationResults'].keys())
        for metric in sumByMetric.keys():
            result['scoreResults'][solveMetricMistake(metric)] = round(sumByMetric[metric] / (relationNumber * 2), 6)
    return calcScore(result['scoreResults'])


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
relation2idPath = parentDir + '/benchmarks/%s/relation2id.txt' % database
f = open(relation2idPath, 'r')
s = f.readlines()
f.close()

relationMap = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) == 2:
        relationMap[splited[1][:-1]] = splited[0]

method = parsedArgs.method if parsedArgs.method else 'TransE'
metricMistake = False
resultPath = parentDir + '/log/%s/%s.log' % (database, method)
f = open(resultPath, 'r')
s = f.readlines()
f.close()

last = 0
rawResults = []
for i in range(len(s)):
    if '-' * 50 in s[i]:
        rawResults.append(s[last:i])
        last = i + 1

ignoredParams = {'nbatches', 'weighted'}
results = dict()
for rawResult in rawResults:
    seqNum = int(rawResult[0].split('_')[1])
    results[seqNum] = dict()
    results[seqNum]['parameters'] = dict()
    results[seqNum]['averageResults'] = dict()
    results[seqNum]['relationResults'] = dict()
    results[seqNum]['time'] = float(rawResult[-2].split(' ')[2])

    i = 1
    while True:
        if not '--' in rawResult[i]:
            break
        parameterName = rawResult[i].split(':')[0].split('--')[1]
        parameterValue = rawResult[i].split(':')[1].strip(' \t\n')
        i += 1
        if parameterName in ignoredParams:
            continue
        if '.' in parameterValue:
            parameterValue = float(parameterValue)
        else:
            parameterValue = int(parameterValue)
        results[seqNum]['parameters'][parameterName] = parameterValue

    metrics = []
    for i in range(len(rawResult)):
        if 'metric:' in rawResult[i]:
            splited = rawResult[i].split('\t')
            for j in range(len(splited)):
                each = splited[j].strip(' \t\n')
                if len(each) > 0 and not ':' in each:
                    metrics.append(each)

        if 'averaged(filter)' in rawResult[i]:
            splited = rawResult[i].split('\t')
            k = 0
            for j in range(len(splited)):
                each = splited[j].strip(' \t\n')
                if len(each) > 0 and not ':' in each:
                    results[seqNum]['averageResults'][metrics[k]] = float(each)
                    k += 1
            break

    for i in range(len(rawResult)):
        if 'Relation' in rawResult[i]:
            relationId = rawResult[i].split(':')[0].strip(' \t\nRelation')
            relationName = relationMap[relationId]
            results[seqNum]['relationResults'][relationName] = dict()

        if 'Prediction:' in rawResult[i]:
            predictEntity = rawResult[i].split('Prediction:')[0].strip(' \t\n')
            results[seqNum]['relationResults'][relationName][predictEntity] = dict()
            splited = rawResult[i].split('\t')
            k = 0
            for j in range(len(splited)):
                each = splited[j].strip(' \t\n')
                if len(each) > 0 and not ':' in each:
                    results[seqNum]['relationResults'][relationName][predictEntity][metrics[k]] = float(each)
                    k += 1

fileSavePath = parentDir + '/log/%s/analyzed/%s_analyzed.log' % (database, method)
f = codecs.open(fileSavePath, 'w', 'utf-8')
sortedResults = sorted(results.keys(), key=lambda x: score(results[x]), reverse=True)
for i in range(len(sortedResults)):
    output(f, i + 1)
    output(f, 'seqNum: ' + str(sortedResults[i]))
    output(f, 'score: ' + str(round(score(results[sortedResults[i]]), 6)))
    output(f, 'time: ' + str(results[sortedResults[i]]['time']))
    output(f, results[sortedResults[i]]['parameters'])
    output(f, results[sortedResults[i]]['scoreResults'])
    for relationName in relationMap.values():
        output(f, relationName + ': ', end='')
        output(f, results[sortedResults[i]]['relationResults'][relationName])
    output(f)

parameterMetric = dict()
for seqNum in results.keys():
    for metric in list(results[seqNum]['scoreResults'].keys()) + ['time', 'score']:
        for parameterName in results[seqNum]['parameters'].keys():
            if parameterMetric.get(parameterName, 0) == 0:
                parameterMetric[parameterName] = dict()
            parameterValue = results[seqNum]['parameters'][parameterName]
            if parameterMetric[parameterName].get(parameterValue, 0) == 0:
                parameterMetric[parameterName][parameterValue] = dict()
            if parameterMetric[parameterName][parameterValue].get(metric, 0) == 0:
                parameterMetric[parameterName][parameterValue][metric] = []
            if not metric in ['time', 'score']:
                parameterMetric[parameterName][parameterValue][metric].append(results[seqNum]['scoreResults'][metric])
            elif metric == 'time':
                parameterMetric[parameterName][parameterValue][metric].append(results[seqNum]['time'])
            elif metric == 'score':
                parameterMetric[parameterName][parameterValue][metric].append(score(results[seqNum]))

for parameterName in sorted(parameterMetric.keys()):
    for parameterValue in sorted(parameterMetric[parameterName].keys()):
        output(f, buildEquation(parameterName, parameterValue))
        for metric in sorted(parameterMetric[parameterName][parameterValue].keys()):
            output(f, '\t' + metric + ' ' * (7 - len(metric))
                   + buildEquation('Average', average(parameterMetric[parameterName][parameterValue][metric])) + '\t'
                   + buildEquation('Max', max(parameterMetric[parameterName][parameterValue][metric])) + '\t'
                   + buildEquation('Min', min(parameterMetric[parameterName][parameterValue][metric])))
        output(f)


def outputAsLatexForSortedResults(sortedResults, results):
    for i in [0, 1, 2, -3, -2, -1] if len(sortedResults) >= 10 else range(len(sortedResults)):
        output(f, '\t', end='')
        output(f, i + 1 if i >= 0 else len(sortedResults) + i + 1, end=' ')
        for parameterName in sorted(results[sortedResults[i]]['parameters'].keys()):
            output(f,
                   '& ' + parameterValueToString(results[sortedResults[i]]['parameters'][parameterName], parameterName),
                   end=' ')
        for metric in [('MRR', 4), ('hit@10', 4), ('hit@3', 4), ('hit@1', 4)]:
            output(f, '& ' + formattedRound(results[sortedResults[i]]['scoreResults'][metric[0]], metric[1]), end=' ')
        output(f, '& ' + formattedRound(results[sortedResults[i]]['time'], 0), end=' ')
        output(f, '& ' + formattedRound(score(results[sortedResults[i]]), 3), end=' ')
        output(f, '\\\\')
    output(f)


def outputAsLatexForAverageResults(parameterMetric):
    for parameterName in sorted(parameterMetric.keys()):
        if len(parameterMetric[parameterName]) <= 1:
            continue
        for parameterValue in sorted(parameterMetric[parameterName].keys()):
            output(f, '\t', end='')
            output(f, '$\\mathrm{' + parameterName + '}=' + str(parameterValue) + '$', end=' ')
            for metric in [('MRR', 4), ('hit@10', 4), ('hit@3', 4), ('hit@1', 4), ('time', 0), ('score', 3)]:
                output(f, '& ' + str(
                    formattedRound(average(parameterMetric[parameterName][parameterValue][metric[0]]), metric[1])),
                       end=' ')
            output(f, '\\\\')
    output(f)


def outputAsLatexForRelationResults(relationResults):
    relations = [('paper_is_written_by', 'paper\_is\_written\_by\_author'),
                 ('paper_is_in_field', 'paper\_is\_in\_field'),
                 ('paper_publish_on', 'paper\_publish\_on\_venue'),
                 ('paper_cit_paper', 'paper\_cite\_paper'),
                 ('work_in', 'author\_work\_in\_institute'),
                 ('author_is_in_field', 'author\_is\_in\_field'),
                 ('field_is_part_of', 'field\_is\_part\_of\_field')]
    typeCHN = {'paper': '论文', 'author': '学者', 'venue': '期刊/会议', 'institute': '机构', 'field': '领域'}
    for i in range(len(relations)):
        head = relationResults[relations[i][0]]['Head']
        tail = relationResults[relations[i][0]]['Tail']
        output(f, '\t\multirow{2}{*}{%s} & 头实体 & %s & %s & %s & %s & %s & %s \\\\'
               % (relations[i][1],
                  typeCHN[relations[i][1].split('\\')[0]],
                  formattedRound(head['MRR'], 4),
                  formattedRound(head['hit@10'], 4),
                  formattedRound(head['hit@3'], 4),
                  formattedRound(head['hit@1'], 4),
                  formattedRound(calcScore(head), 3))
               )
        output(f, '\t& 尾实体 & %s & %s & %s & %s & %s & %s \\\\'
               % (typeCHN[relations[i][1].split('_')[-1]],
                  formattedRound(tail['MRR'], 4),
                  formattedRound(tail['hit@10'], 4),
                  formattedRound(tail['hit@3'], 4),
                  formattedRound(tail['hit@1'], 4),
                  formattedRound(calcScore(tail), 3))
               )


outputAsLatexForSortedResults(sortedResults, results)
outputAsLatexForAverageResults(parameterMetric)
outputAsLatexForRelationResults(results[sortedResults[0]]['relationResults'])

f.close()
