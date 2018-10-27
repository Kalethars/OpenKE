def average(list):
    return float(sum(list)) / len(list)


def buildEquation(name, value):
    return str(name) + ' = ' + str(round(value, 6))


def score(averageResult):
    return averageResult['hit@10'] + averageResult['hit@3'] + averageResult['hit@1'] + averageResult['MRR']


dataset = 'ACE17K'
relation2idPath = '../benchmarks/%s/relation2id.txt' % dataset
f = open(relation2idPath, 'r')
s = f.readlines()
f.close()

relationMap = dict()
for line in s:
    splited = line.split('\t')
    if len(splited) == 2:
        relationMap[splited[1][:-1]] = splited[0]

method = 'TransE'
resultPath = '../log/%s.log' % method
f = open(resultPath, 'r')
s = f.readlines()
f.close()

rawResults = []
for i in range(len(s)):
    if '-' * 50 in s[i]:
        rawResults.append(s[i - 42:i])

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
        if '.' in parameterValue:
            parameterValue = float(parameterValue)
        else:
            parameterValue = int(parameterValue)
        results[seqNum]['parameters'][parameterName] = parameterValue
        i += 1

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

sortedResults = sorted(results.keys(), key=lambda x: score(results[x]['averageResults']), reverse=True)
for i in range(len(sortedResults)):
    print(i + 1)
    print('seqNum: ' + str(sortedResults[i]))
    print('score: ' + str(round(score(results[sortedResults[i]]['averageResults']), 6)))
    print('time: ' + str(results[sortedResults[i]]['time']))
    print(results[sortedResults[i]]['parameters'])
    print(results[sortedResults[i]]['averageResults'])
    for relationName in relationMap.values():
        print(relationName + ': ', end='')
        print(results[sortedResults[i]]['relationResults'][relationName])
    print()

parameterMetric = dict()
for seqNum in results.keys():
    for metric in list(results[seqNum]['averageResults'].keys()) + ['time', 'score']:
        for parameterName in results[seqNum]['parameters'].keys():
            if parameterMetric.get(parameterName, 0) == 0:
                parameterMetric[parameterName] = dict()
            parameterValue = results[seqNum]['parameters'][parameterName]
            if parameterMetric[parameterName].get(parameterValue, 0) == 0:
                parameterMetric[parameterName][parameterValue] = dict()
            if parameterMetric[parameterName][parameterValue].get(metric, 0) == 0:
                parameterMetric[parameterName][parameterValue][metric] = []
            if not metric in ['time', 'score']:
                parameterMetric[parameterName][parameterValue][metric].append(results[seqNum]['averageResults'][metric])
            elif metric == 'time':
                parameterMetric[parameterName][parameterValue][metric].append(results[seqNum]['time'])
            elif metric == 'score':
                parameterMetric[parameterName][parameterValue][metric].append(score(results[seqNum]['averageResults']))

for parameterName in sorted(parameterMetric.keys()):
    for parameterValue in sorted(parameterMetric[parameterName].keys()):
        print(buildEquation(parameterName, parameterValue))
        for metric in sorted(parameterMetric[parameterName][parameterValue].keys()):
            print('\t' + metric + ' ' * (7 - len(metric))
                  + buildEquation('Average', average(parameterMetric[parameterName][parameterValue][metric])) + '\t'
                  + buildEquation('Max', max(parameterMetric[parameterName][parameterValue][metric])) + '\t'
                  + buildEquation('Min', min(parameterMetric[parameterName][parameterValue][metric])))
        print()


def outputAsLatex(parameterMetric):
    for parameterName in sorted(parameterMetric.keys()):
        for parameterValue in sorted(parameterMetric[parameterName].keys()):
            print('$\\mathrm{' + parameterName + '}=' + str(parameterValue) + '$ ', end='')
            for metric in [('MRR', 4), ('hit@10', 4), ('hit@3', 4), ('hit@1', 4), ('time', 0), ('score', 3)]:
                print('& ' + str(
                    round(average(parameterMetric[parameterName][parameterValue][metric[0]]), metric[1])) + ' ',
                      end='')
            print('\\\\')


outputAsLatex(parameterMetric)
