def formattedRound(number, digit):
    if digit == 0:
        return str(round(number))
    else:
        rounded = str(round(number, digit))
        if not '.' in rounded:
            rounded = rounded + '.'
        return rounded + (digit - len(rounded.split('.')[1])) * '0'


methods = ['TransE_detailed/6', 'TransH_test/1', 'DistMult_detailed/1', 'ComplEx_advanced/2']
algs = [('mindist', '$f_r(h,t)$'), ('normdist', '$z_r(h,t)$'), ('maxmrr', '$R_r^{-1}(h,t)$')]
coeffs = ['0.1', '0.05']
metrics = ['MRR', 'Hit@10', 'Hit@3', 'Hit@1', 'Score']

for method in methods:
    print('\\midrule')

    bestAuthorVenue = dict()
    bestpaperInsitute = dict()
    authorVenue = dict()
    paperInsitute = dict()
    for (alg, func) in algs:
        authorVenue[alg] = dict()
        paperInsitute[alg] = dict()
        betterScore={'authorVenue':0, 'paperInstitute':0}
        for coeff in coeffs:
            analyzedPath = '../../res/ACE17K/%s/recommendation/analyzed/%s_prediction_analysis_coeff=%s.log' % (
                method, alg, coeff)
            f = open(analyzedPath, 'r')
            s = f.read().split('\n\n')
            f.close()

            for part in s:
                lines = part.split('\n')
                if lines[0] == 'Predict venue for author:':
                    ref = authorVenue[alg]
                    bestRef = bestAuthorVenue
                    scoreRef='authorVenue'
                elif lines[0] == 'Predict institute for paper:':
                    ref = paperInsitute[alg]
                    bestRef = bestpaperInsitute
                    scoreRef='paperInstitute'
                else:
                    continue
                if float(lines[-1].split()[-1]) > betterScore[scoreRef]:
                    betterScore[scoreRef] = float(lines[-1].split()[-1])
                    for i in range(1, len(lines)):
                        splited = lines[i].split(':\t')
                        metric = splited[0]
                        digit = 4 if metric != 'Score' else 3
                        value = formattedRound(float(splited[1]), digit)
                        ref[metric] = value
                        bestRef[metric] = formattedRound(max(float(bestRef.get(metric, 0)), float(value)), digit)

    for (alg, func) in algs:
        output = '\multirow{%i}{*}{%s} & ' % (len(algs), (method.split('_')[0])) if alg == 'mindist' else '& '
        output += '%s' % func
        for metric in metrics:
            if authorVenue[alg][metric] == bestAuthorVenue[metric]:
                output += ' & \\textbf{%s}' % authorVenue[alg][metric]
            else:
                output += ' & %s' % authorVenue[alg][metric]
        for metric in metrics:
            if paperInsitute[alg][metric] == bestpaperInsitute[metric]:
                output += ' & \\textbf{%s}' % paperInsitute[alg][metric]
            else:
                output += ' & %s' % paperInsitute[alg][metric]
        output += ' \\\\'
        print(output)
