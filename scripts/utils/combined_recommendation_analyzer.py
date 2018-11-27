import argparse
import os

try:
    import win_unicode_console

    win_unicode_console.enable()
except:
    pass

parentDir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def getBestOrder(database, method):
    try:
        analyzedLogPath = parentDir + '/log/%s/analyzed/%s_analyzed.log' % (database, method)
        f = open(analyzedLogPath, 'r')
        s = f.read().split('\n')
        f.close()

        bestOrder = int(s[1].split()[1])
        return bestOrder
    except:
        return 1


def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


def paperInstituteAnalyzer():
    f = open(parentDir + '/res/%s/%s/%i/recommendation/combinedRecommendation_paper_institute.txt'
             % (database, method, order), 'r')
    s = f.read().split('\n')
    f.close()

    recommendation = dict()
    for i in range(len(s)):
        if '-' * 50 in s[i]:
            paperId = s[i - 1].split()[1]

            recommendation[paperId] = dict()
            for j in range(count):
                splited = s[i + j + 1].split()
                if len(splited) < 2:
                    continue
                recommendationId = splited[0]
                recommendation[paperId][recommendationId] = j + 1

    f = open(parentDir + '/data/%s/PaperAuthorAffiliations.data' % database, 'r')
    s = f.read().split('\n')
    f.close()

    hitAt = [10, 3, 1]
    hitAtValue = dict()
    cnt = 0
    for line in s:
        splited = line.split()
        if len(splited) != 4:
            continue
        if len(splited[2]) != 8:
            continue
        rank = recommendation[splited[0]].get(splited[2], 11)
        for num in hitAt:
            if rank <= num:
                hitAtValue[num] = hitAtValue.get(num, 0) + 1
        cnt += 1

    for num in hitAt:
        hitAtValue[num] = hitAtValue.get(num, 0) / cnt
        print('Hit@%i: %s' % (num, formattedRound(hitAtValue[num], 4)))


parser = argparse.ArgumentParser()
parser.add_argument('--database', type=str, required=False)
parser.add_argument('--method', type=str, required=True)
parser.add_argument('--order', type=int, required=False)
parser.add_argument('--count', type=int, required=False)
parsedArgs = parser.parse_args()

database = parsedArgs.database if parsedArgs.database else 'ACE17K'
method = parsedArgs.method
order = parsedArgs.order if parsedArgs.order else getBestOrder(database, method)
count = parsedArgs.count if parsedArgs.count else 10

paperInstituteAnalyzer()
