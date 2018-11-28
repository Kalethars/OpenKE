#ifndef TEST_H
#define TEST_H
#include "Setting.h"
#include "Reader.h"
#include "Corrupt.h"
/*=====================================================================================
entity recommendation
======================================================================================*/
INT lastRecommend = 0;

extern "C"
void getRecommendBatch(INT *ph, INT *pt, INT *pr, REAL *pw) {
    for (INT i = 0; i < entityTotal; i++) {
        if (recommendList[lastRecommend].h == -1) {
            ph[i] = i;
            pt[i] = recommendList[lastRecommend].t;
        } else {
            ph[i] = recommendList[lastRecommend].h;
            pt[i] = i;
        }
        pr[i] = recommendList[lastRecommend].r;
        pw[i] = recommendList[lastRecommend].w;
    }
}

struct PAIR {
	INT key;
	REAL value;

	static bool cmp_value(const PAIR &a, const PAIR &b) {
		return (a.value < b.value);
	}
};

extern "C"
void recommend(REAL *con, INT recommendCount, const char* output) {
    INT h = recommendList[lastRecommend].h;
    INT t = recommendList[lastRecommend].t;
    INT r = recommendList[lastRecommend].r;

    PAIR* candidates;
    INT candidateTotal;

    FILE* fp = fopen(output, "a");
    if (h == -1) {
        candidateTotal = head_rig[r] - head_lef[r];
        candidates = (PAIR *)calloc(candidateTotal, sizeof(PAIR));

        for (INT i = head_lef[r]; i < head_rig[r]; i++) {
            candidates[i - head_lef[r]].key = head_type[i];
            candidates[i - head_lef[r]].value = con[head_type[i]];
        }
        std::sort(candidates, candidates + candidateTotal, PAIR::cmp_value);

        if (recommendCount <= 0) {
            recommendCount = candidateTotal;
        }

        fprintf(fp, "Case %ld. Recommend head entity. Given tail = %ld, relation = %ld, count = %ld.\n",
                lastRecommend + 1, t, r, recommendCount);
        printf("Case %ld. Recommend head entity. Given tail = %ld, relation = %ld.\n", lastRecommend + 1, t, r);

        INT j = 0;
        for (INT i = 0; i < recommendCount; i++) {
            while (_find(candidates[j].key, t, r) || t == candidates[j].key) {
                j++;
            }
            fprintf(fp, "\t%ld\t%ld\t%.4f\n", candidates[j].key, j + 1, candidates[j].value);
            j++;
        }
    } else {
        candidateTotal = tail_rig[r] - tail_lef[r];
        candidates = (PAIR *)calloc(candidateTotal, sizeof(PAIR));

        for (INT i = tail_lef[r]; i < tail_rig[r]; i++) {
            candidates[i - tail_lef[r]].key = tail_type[i];
            candidates[i - tail_lef[r]].value = con[tail_type[i]];
        }
        std::sort(candidates, candidates + candidateTotal, PAIR::cmp_value);

        if (recommendCount <= 0) {
            recommendCount = candidateTotal;
        }

        fprintf(fp, "Case %ld. Recommend tail entity. Given head = %ld, relation = %ld, count = %ld.\n",
                lastRecommend + 1, h, r, recommendCount);
        printf("Case %ld. Recommend tail entity. Given head = %ld, relation = %ld.\n", lastRecommend + 1, h, r);

        INT j = 0;
        for (INT i = 0; i < recommendCount; i++) {
            while (_find(h, candidates[j].key, r) || h == candidates[j].key) {
                j++;
            }
            fprintf(fp, "\t%ld\t%ld\t%.4f\n", candidates[j].key, j + 1, candidates[j].value);
            j++;
        }
    }
    lastRecommend++;

    fclose(fp);
}

/*=====================================================================================
link prediction
======================================================================================*/
INT lastHead = 0;
INT lastTail = 0;
REAL l1_filter_tot = 0, l1_tot = 0, r1_tot = 0, r1_filter_tot = 0, l_tot = 0, r_tot = 0, l_filter_rank = 0, l_rank = 0, l_filter_reci_rank = 0, l_reci_rank = 0;
REAL l3_filter_tot = 0, l3_tot = 0, r3_tot = 0, r3_filter_tot = 0, l_filter_tot = 0, r_filter_tot = 0, r_filter_rank = 0, r_rank = 0, r_filter_reci_rank = 0, r_reci_rank = 0;

extern "C"
void getHeadBatch(INT *ph, INT *pt, INT *pr, REAL *pw) {
    for (INT i = 0; i < entityTotal; i++) {
        ph[i] = i;
        pt[i] = testList[lastHead].t;
        pr[i] = testList[lastHead].r;
        pw[i] = testList[lastHead].w;
    }
}

extern "C"
void getTailBatch(INT *ph, INT *pt, INT *pr, REAL *pw) {
    for (INT i = 0; i < entityTotal; i++) {
        ph[i] = testList[lastTail].h;
        pt[i] = i;
        pr[i] = testList[lastTail].r;
        pw[i] = testList[lastTail].w;
    }
}

extern "C"
void testHead(REAL *con, bool weighted = false) {
    INT h = testList[lastHead].h;
    INT t = testList[lastHead].t;
    INT r = testList[lastHead].r;
    REAL w;
    if (weighted) {
        w = testList[lastHead].w;
    } else {
        w = 1.0;
    }

    REAL minimal = con[h];
    INT l_s = 1;
    INT l_filter_s = 1;

    for (INT i = head_lef[r]; i < head_rig[r]; i++) {
        INT j = head_type[i];
        REAL value = con[j];
        if ((j != h) && (j != t)) {
            if (value < minimal) {
                l_s += 1;
            }
            if (not _find(j, t, r)) {
                if (value < minimal) {
                    l_filter_s += 1;
                }
            }
        }
    }

    relationCount[r] += 1;

    if (l_filter_s <= 10) {
        l_filter_tot += w;
        hitAt10[r] += w;
    }
    if (l_s <= 10) l_tot += w;
    if (l_filter_s <= 3) {
        l3_filter_tot += w;
        hitAt3[r] += w;
    }
    if (l_s <= 3) l3_tot += w;
    if (l_filter_s <= w) {
        l1_filter_tot += w;
        hitAt1[r] += w;
    }
    if (l_s <= 1) l1_tot += w;
    l_filter_rank += l_filter_s / w;
    meanRank[r] += l_filter_s / w;
    l_rank += l_s / w;
    l_filter_reci_rank += w / l_filter_s;
    meanRankReciprocal[r] += w / l_filter_s;
    l_reci_rank += w / l_s;
    lastHead++;
    printf("h: %ld r: %ld t: %ld value: %f\n", h, r, t, minimal);
    printf("l_filter_s: %ld\t", l_filter_s);
    // printf("%f %f %f %f \n", l_tot / lastHead, l_filter_tot / lastHead, l_rank / lastHead, l_filter_rank / lastHead);
}

extern "C"
void testTail(REAL *con, bool weighted = false) {
    INT h = testList[lastTail].h;
    INT t = testList[lastTail].t;
    INT r = testList[lastTail].r;
    REAL w;
    if (weighted) {
        w = testList[lastTail].w;
    } else {
        w = 1.0;
    }

    REAL minimal = con[t];
    INT r_s = 1;
    INT r_filter_s = 1;

    for (INT i = tail_lef[r]; i < tail_rig[r]; i++) {
        INT j = tail_type[i];
        REAL value = con[j];
        if ((j != h) && (j != t)) {
            if (value < minimal) {
                r_s += 1;
            }
            if (not _find(h, j, r)) {
                if (value < minimal) {
                    r_filter_s += 1;
                }
            }
        }
    }

    relationCount[relationTotal+r] += 1;

    if (r_filter_s <= 10) {
        r_filter_tot += w;
        hitAt10[relationTotal+r] += w;
    }
    if (r_s <= 10) r_tot += w;
    if (r_filter_s <= 3) {
        r3_filter_tot += w;
        hitAt3[relationTotal+r] += w;
    }
    if (r_s <= 3) r3_tot += w;
    if (r_filter_s <= 1) {
        r1_filter_tot += w;
        hitAt1[relationTotal+r] += w;
    }
    if (r_s <= 1) r1_tot += w;
    r_filter_rank += r_filter_s / w;
    meanRank[relationTotal+r] += r_filter_s / w;
    r_rank += r_s / w;
    r_filter_reci_rank += w / r_filter_s;
    meanRankReciprocal[relationTotal+r] += w / r_filter_s;
    r_reci_rank += w / r_s;
    lastTail++;
    // printf("h: %ld r: %ld t:%ld value:%f\n", h, r, t, minimal);
    printf("r_filter_s: %ld\n\n", r_filter_s);
    // printf("%f %f %f %f\n", r_tot /lastTail, r_filter_tot /lastTail, r_rank /lastTail, r_filter_rank /lastTail);
}

extern "C"
void test_link_prediction(const char* output) {
    l_rank /= testTotal;
    r_rank /= testTotal;
    l_reci_rank /= testTotal;
    r_reci_rank /= testTotal;
 
    l_tot /= testTotal;
    l3_tot /= testTotal;
    l1_tot /= testTotal;
 
    r_tot /= testTotal;
    r3_tot /= testTotal;
    r1_tot /= testTotal;

    // with filter
    l_filter_rank /= testTotal;
    r_filter_rank /= testTotal;
    l_filter_reci_rank /= testTotal;
    r_filter_reci_rank /= testTotal;
 
    l_filter_tot /= testTotal;
    l3_filter_tot /= testTotal;
    l1_filter_tot /= testTotal;
 
    r_filter_tot /= testTotal;
    r3_filter_tot /= testTotal;
    r1_filter_tot /= testTotal;

    // relation specific
    for (INT i = 0; i < relationTotal*2; i++){
        meanRank[i] /= relationCount[i];
        meanRankReciprocal[i] /= relationCount[i];
        hitAt10[i] /= relationCount[i];
        hitAt3[i] /= relationCount[i];
        hitAt1[i] /= relationCount[i];
    }

    FILE* fp=fopen(output, "a");
    fprintf(fp,"Overall results:\n");
    
    fprintf(fp,"metric:\t\t\t MRR \t\t MR \t\t hit@10 \t hit@3  \t hit@1 \n");
    fprintf(fp,"l(raw):\t\t\t %f \t %f \t %f \t %f \t %f \n", l_reci_rank, l_rank, l_tot, l3_tot, l1_tot);
    fprintf(fp,"r(raw):\t\t\t %f \t %f \t %f \t %f \t %f \n", r_reci_rank, r_rank, r_tot, r3_tot, r1_tot);
    fprintf(fp,"averaged(raw):\t\t %f \t %f \t %f \t %f \t %f \n",
            (l_reci_rank+r_reci_rank)/2, (l_rank+r_rank)/2, (l_tot+r_tot)/2, (l3_tot+r3_tot)/2, (l1_tot+r1_tot)/2);
    fprintf(fp,"\n");
    fprintf(fp,"l(filter):\t\t %f \t %f \t %f \t %f \t %f \n", l_filter_reci_rank, l_filter_rank, l_filter_tot, l3_filter_tot, l1_filter_tot);
    fprintf(fp,"r(filter):\t\t %f \t %f \t %f \t %f \t %f \n", r_filter_reci_rank, r_filter_rank, r_filter_tot, r3_filter_tot, r1_filter_tot);
    fprintf(fp,"averaged(filter):\t %f \t %f \t %f \t %f \t %f \n",
            (l_filter_reci_rank+r_filter_reci_rank)/2, (l_filter_rank+r_filter_rank)/2, (l_filter_tot+r_filter_tot)/2, (l3_filter_tot+r3_filter_tot)/2, (l1_filter_tot+r1_filter_tot)/2);
    fprintf(fp,"\n");
    for (INT i = 0; i < relationTotal; i++) {
        fprintf(fp,"Relation %ld:\t\t\t MRR \t\t MR \t\t hit@10 \t hit@3  \t hit@1 \n", i);
        fprintf(fp,"Head Prediction:\t\t %f \t %f \t %f \t %f \t %f \n",
                meanRankReciprocal[i],
                meanRank[i],
                hitAt10[i],
                hitAt3[i],
                hitAt1[i]
        );
        fprintf(fp,"Tail Prediction:\t\t %f \t %f \t %f \t %f \t %f \n",
                meanRankReciprocal[relationTotal+i],
                meanRank[relationTotal+i],
                hitAt10[relationTotal+i],
                hitAt3[relationTotal+i],
                hitAt1[relationTotal+i]
        );
    }
    fclose(fp);
}

/*=====================================================================================
triple classification
======================================================================================*/
Triple *negTestList;
extern "C"
void getNegTest() {
    negTestList = (Triple *)calloc(testTotal, sizeof(Triple));
    for (INT i = 0; i < testTotal; i++) {
        negTestList[i] = testList[i];
        negTestList[i].t = corrupt(testList[i].h, testList[i].r);
    }
    FILE* fout = fopen((inPath + "test_neg.txt").c_str(), "w");
    for (INT i = 0; i < testTotal; i++) {
        fprintf(fout, "%ld\t%ld\t%ld\t%ld\n", testList[i].h, testList[i].t, testList[i].r, INT(1));
        fprintf(fout, "%ld\t%ld\t%ld\t%ld\n", negTestList[i].h, negTestList[i].t, negTestList[i].r, INT(-1));
    }
    fclose(fout);
}

Triple *negValidList;
extern "C"
void getNegValid() {
    negValidList = (Triple *)calloc(validTotal, sizeof(Triple));
    for (INT i = 0; i < validTotal; i++) {
        negValidList[i] = validList[i];
        negValidList[i].t = corrupt(validList[i].h, validList[i].r);
    }
    FILE* fout = fopen((inPath + "valid_neg.txt").c_str(), "w");
    for (INT i = 0; i < validTotal; i++) {
        fprintf(fout, "%ld\t%ld\t%ld\t%ld\n", validList[i].h, validList[i].t, validList[i].r, INT(1));
        fprintf(fout, "%ld\t%ld\t%ld\t%ld\n", negValidList[i].h, negValidList[i].t, negValidList[i].r, INT(-1));
    }
    fclose(fout);
        
}

extern "C"
void getTestBatch(INT *ph, INT *pt, INT *pr, INT *nh, INT *nt, INT *nr) {
    getNegTest();
    for (INT i = 0; i < testTotal; i++) {
        ph[i] = testList[i].h;
        pt[i] = testList[i].t;
        pr[i] = testList[i].r;
        nh[i] = negTestList[i].h;
        nt[i] = negTestList[i].t;
        nr[i] = negTestList[i].r;
    }
}

extern "C"
void getValidBatch(INT *ph, INT *pt, INT *pr, INT *nh, INT *nt, INT *nr) {
    getNegValid();
    for (INT i = 0; i < validTotal; i++) {
        ph[i] = validList[i].h;
        pt[i] = validList[i].t;
        pr[i] = validList[i].r;
        nh[i] = negValidList[i].h;
        nt[i] = negValidList[i].t;
        nr[i] = negValidList[i].r;
    }
}

REAL *relThresh;
REAL threshEntire;
extern "C"
void getBestThreshold(REAL *score_pos, REAL *score_neg) {
    REAL interval = 0.01;
    relThresh = (REAL *)calloc(relationTotal, sizeof(REAL));
    REAL min_score, max_score, bestThresh, tmpThresh, bestAcc, tmpAcc;
    INT n_interval, correct, total;
    for (INT r = 0; r < relationTotal; r++) {
        if (validLef[r] == -1) continue;
        total = (validRig[r] - validLef[r] + 1) * 2;
        min_score = score_pos[validLef[r]];
        if (score_neg[validLef[r]] < min_score) min_score = score_neg[validLef[r]];
        max_score = score_pos[validLef[r]];
        if (score_neg[validLef[r]] > max_score) max_score = score_neg[validLef[r]];
        for (INT i = validLef[r]+1; i <= validRig[r]; i++) {
            if(score_pos[i] < min_score) min_score = score_pos[i];
            if(score_pos[i] > max_score) max_score = score_pos[i];
            if(score_neg[i] < min_score) min_score = score_neg[i];
            if(score_neg[i] > max_score) max_score = score_neg[i];
        }
        n_interval = INT((max_score - min_score)/interval);
        for (INT i = 0; i <= n_interval; i++) {
            tmpThresh = min_score + i * interval;
            correct = 0;
            for (INT j = validLef[r]; j <= validRig[r]; j++) {
                if (score_pos[j] <= tmpThresh) correct ++;
                if (score_neg[j] > tmpThresh) correct ++;
            }
            tmpAcc = 1.0 * correct / total;
            if (i == 0) {
                bestThresh = tmpThresh;
                bestAcc = tmpAcc;
            } else if (tmpAcc > bestAcc) {
                bestAcc = tmpAcc;
                bestThresh = tmpThresh;
            }
        }
        relThresh[r] = bestThresh;
       // printf("relation %ld: bestThresh is %lf, bestAcc is %lf\n", r, bestThresh, bestAcc);
    }
}

REAL *testAcc;
REAL aveAcc;
extern "C"
void test_triple_classification(REAL *score_pos, REAL *score_neg) {
    testAcc = (REAL *)calloc(relationTotal, sizeof(REAL));
    INT aveCorrect = 0, aveTotal = 0;
    REAL aveAcc;
    for (INT r = 0; r < relationTotal; r++) {
        if (validLef[r] == -1 || testLef[r] ==-1) continue;
        INT correct = 0, total = 0;
        for (INT i = testLef[r]; i <= testRig[r]; i++) {
            if (score_pos[i] <= relThresh[r]) correct++;
            if (score_neg[i] > relThresh[r]) correct++;
            total += 2;
        }
        printf("%ld",total);
        testAcc[r] = 1.0 * correct / total;
        aveCorrect += correct; 
        aveTotal += total;
    //    printf("relation %ld: triple classification accuracy is %lf\n", r, testAcc[r]);
    }
    aveAcc = 1.0 * aveCorrect / aveTotal;
    printf("triple classification accuracy is %lf\n", aveAcc);
}

#endif
