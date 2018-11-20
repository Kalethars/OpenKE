#ifndef READER_H
#define READER_H
#include "Setting.h"
#include "Triple.h"
#include <cstdlib>
#include <algorithm>

INT *freqRel, *freqEnt;
INT *lefHead, *rigHead;
INT *lefTail, *rigTail;
INT *lefRel, *rigRel;
REAL *left_mean, *right_mean;

Triple *trainList;
Triple *trainHead;
Triple *trainTail;
Triple *trainRel;

INT *testLef, *testRig;
INT *validLef, *validRig;

// Only "filter" result is counted
REAL *meanRank, *meanRankReciprocal, *hitAt10, *hitAt3, *hitAt1;
INT *relationCount;

extern "C"
void importTrainFiles() {
	printf("The toolkit is importing datasets.\n");
	FILE *fin;
	int tmp;

	fin = fopen((inPath + "relation2id.txt").c_str(), "r");
	tmp = fscanf(fin, "%ld", &relationTotal);
	printf("The total of relations is %ld.\n", relationTotal);
	fclose(fin);

	fin = fopen((inPath + "entity2id.txt").c_str(), "r");
	tmp = fscanf(fin, "%ld", &entityTotal);
	printf("The total of entities is %ld.\n", entityTotal);
	fclose(fin);

    fin = fopen((inPath + "train2id_weighted.txt").c_str(), "r");
	tmp = fscanf(fin, "%ld", &trainTotal);
	trainList = (Triple *)calloc(trainTotal, sizeof(Triple));
	trainHead = (Triple *)calloc(trainTotal, sizeof(Triple));
	trainTail = (Triple *)calloc(trainTotal, sizeof(Triple));
	trainRel = (Triple *)calloc(trainTotal, sizeof(Triple));
	freqRel = (INT *)calloc(relationTotal, sizeof(INT));
	freqEnt = (INT *)calloc(entityTotal, sizeof(INT));
	for (INT i = 0; i < trainTotal; i++) {
		tmp = fscanf(fin, "%ld", &trainList[i].h);
		tmp = fscanf(fin, "%ld", &trainList[i].t);
		tmp = fscanf(fin, "%ld", &trainList[i].r);
		tmp = fscanf(fin, "%f", &trainList[i].w);
	}
	fclose(fin);
	std::sort(trainList, trainList + trainTotal, Triple::cmp_head);
	tmp = trainTotal; trainTotal = 1;
	trainHead[0] = trainTail[0] = trainRel[0] = trainList[0];
	freqEnt[trainList[0].t] += 1;
	freqEnt[trainList[0].h] += 1;
	freqRel[trainList[0].r] += 1;
	for (INT i = 1; i < tmp; i++)
		if (trainList[i].h != trainList[i - 1].h || trainList[i].r != trainList[i - 1].r || trainList[i].t != trainList[i - 1].t) {
			trainHead[trainTotal] = trainTail[trainTotal] = trainRel[trainTotal] = trainList[trainTotal] = trainList[i];
			trainTotal++;
			freqEnt[trainList[i].t]++;
			freqEnt[trainList[i].h]++;
			freqRel[trainList[i].r]++;
		}

	std::sort(trainHead, trainHead + trainTotal, Triple::cmp_head);
	std::sort(trainTail, trainTail + trainTotal, Triple::cmp_tail);
	std::sort(trainRel, trainRel + trainTotal, Triple::cmp_rel);
	printf("The total of train triples is %ld.\n", trainTotal);

	lefHead = (INT *)calloc(entityTotal, sizeof(INT));
	rigHead = (INT *)calloc(entityTotal, sizeof(INT));
	lefTail = (INT *)calloc(entityTotal, sizeof(INT));
	rigTail = (INT *)calloc(entityTotal, sizeof(INT));
	lefRel = (INT *)calloc(entityTotal, sizeof(INT));
	rigRel = (INT *)calloc(entityTotal, sizeof(INT));
	memset(rigHead, -1, sizeof(INT)*entityTotal);
	memset(rigTail, -1, sizeof(INT)*entityTotal);
	memset(rigRel, -1, sizeof(INT)*entityTotal);
	for (INT i = 1; i < trainTotal; i++) {
		if (trainTail[i].t != trainTail[i - 1].t) {
			rigTail[trainTail[i - 1].t] = i - 1;
			lefTail[trainTail[i].t] = i;
		}
		if (trainHead[i].h != trainHead[i - 1].h) {
			rigHead[trainHead[i - 1].h] = i - 1;
			lefHead[trainHead[i].h] = i;
		}
		if (trainRel[i].h != trainRel[i - 1].h) {
			rigRel[trainRel[i - 1].h] = i - 1;
			lefRel[trainRel[i].h] = i;
		}
	}
	lefHead[trainHead[0].h] = 0;
	rigHead[trainHead[trainTotal - 1].h] = trainTotal - 1;
	lefTail[trainTail[0].t] = 0;
	rigTail[trainTail[trainTotal - 1].t] = trainTotal - 1;
	lefRel[trainRel[0].h] = 0;
	rigRel[trainRel[trainTotal - 1].h] = trainTotal - 1;

	left_mean = (REAL *)calloc(relationTotal,sizeof(REAL));
	right_mean = (REAL *)calloc(relationTotal,sizeof(REAL));
	for (INT i = 0; i < entityTotal; i++) {
		for (INT j = lefHead[i] + 1; j < rigHead[i]; j++)
			if (trainHead[j].r != trainHead[j - 1].r)
				left_mean[trainHead[j].r] += 1.0;
		if (lefHead[i] <= rigHead[i])
			left_mean[trainHead[lefHead[i]].r] += 1.0;
		for (INT j = lefTail[i] + 1; j < rigTail[i]; j++)
			if (trainTail[j].r != trainTail[j - 1].r)
				right_mean[trainTail[j].r] += 1.0;
		if (lefTail[i] <= rigTail[i])
			right_mean[trainTail[lefTail[i]].r] += 1.0;
	}
	for (INT i = 0; i < relationTotal; i++) {
		left_mean[i] = freqRel[i] / left_mean[i];
		right_mean[i] = freqRel[i] / right_mean[i];
	}
}

Triple *testList;
Triple *validList;
Triple *tripleList;

extern "C"
void importTestFiles() {
    FILE *fin, *f_kb1, *f_kb2, *f_kb3;
    INT tmp;
    
	fin = fopen((inPath + "relation2id.txt").c_str(), "r");
    tmp = fscanf(fin, "%ld", &relationTotal);
    fclose(fin);

	fin = fopen((inPath + "entity2id.txt").c_str(), "r");
    tmp = fscanf(fin, "%ld", &entityTotal);
    fclose(fin);

    f_kb1 = fopen((inPath + "test2id_weighted.txt").c_str(), "r");
    f_kb2 = fopen((inPath + "train2id_weighted.txt").c_str(), "r");
    f_kb3 = fopen((inPath + "valid2id_weighted.txt").c_str(), "r");
    tmp = fscanf(f_kb1, "%ld", &testTotal);
    tmp = fscanf(f_kb2, "%ld", &trainTotal);
    tmp = fscanf(f_kb3, "%ld", &validTotal);
    tripleTotal = testTotal + trainTotal + validTotal;
    testList = (Triple *)calloc(testTotal, sizeof(Triple));
    validList = (Triple *)calloc(validTotal, sizeof(Triple));
    tripleList = (Triple *)calloc(tripleTotal, sizeof(Triple));
    for (INT i = 0; i < testTotal; i++) {
        tmp = fscanf(f_kb1, "%ld", &tripleList[i].h);
        tmp = fscanf(f_kb1, "%ld", &tripleList[i].t);
        tmp = fscanf(f_kb1, "%ld", &tripleList[i].r);
        tmp = fscanf(f_kb1, "%f", &tripleList[i].w);
        testList[i] = tripleList[i];
    }
    for (INT i = 0; i < trainTotal; i++) {
        tmp = fscanf(f_kb2, "%ld", &tripleList[i + testTotal].h);
        tmp = fscanf(f_kb2, "%ld", &tripleList[i + testTotal].t);
        tmp = fscanf(f_kb2, "%ld", &tripleList[i + testTotal].r);
        tmp = fscanf(f_kb2, "%f", &tripleList[i + testTotal].w);
    }
    for (INT i = 0; i < validTotal; i++) {
        tmp = fscanf(f_kb3, "%ld", &tripleList[i + testTotal + trainTotal].h);
        tmp = fscanf(f_kb3, "%ld", &tripleList[i + testTotal + trainTotal].t);
        tmp = fscanf(f_kb3, "%ld", &tripleList[i + testTotal + trainTotal].r);
        tmp = fscanf(f_kb3, "%f", &tripleList[i + testTotal + trainTotal].w);
        validList[i] = tripleList[i + testTotal + trainTotal];
    }
    fclose(f_kb1);
    fclose(f_kb2);
    fclose(f_kb3);

    std::sort(tripleList, tripleList + tripleTotal, Triple::cmp_head);
    std::sort(testList, testList + testTotal, Triple::cmp_rel2);
    std::sort(validList, validList + validTotal, Triple::cmp_rel2);
    printf("The total of test triples is %ld.\n", testTotal);
    printf("The total of valid triples is %ld.\n", validTotal);

    testLef = (INT *)calloc(relationTotal, sizeof(INT));
	testRig = (INT *)calloc(relationTotal, sizeof(INT));
	memset(testLef, -1, sizeof(INT)*relationTotal);
	memset(testRig, -1, sizeof(INT)*relationTotal);
	for (INT i = 1; i < testTotal; i++) {
		if (testList[i].r != testList[i-1].r) {
			testRig[testList[i-1].r] = i - 1;
			testLef[testList[i].r] = i;
		}
	}
	testLef[testList[0].r] = 0;
	testRig[testList[testTotal - 1].r] = testTotal - 1;

	validLef = (INT *)calloc(relationTotal, sizeof(INT));
	validRig = (INT *)calloc(relationTotal, sizeof(INT));
	memset(validLef, -1, sizeof(INT)*relationTotal);
	memset(validRig, -1, sizeof(INT)*relationTotal);
	for (INT i = 1; i < validTotal; i++) {
		if (validList[i].r != validList[i-1].r) {
			validRig[validList[i-1].r] = i - 1;
			validLef[validList[i].r] = i;
		}
	}
	validLef[validList[0].r] = 0;
	validRig[validList[validTotal - 1].r] = validTotal - 1;

    // Left: 0 ~ relationTotal-1
    // Right: relationTotal ~ 2*relationTotal-1
	meanRank = (REAL *)calloc(relationTotal*2, sizeof(REAL));
	meanRankReciprocal = (REAL *)calloc(relationTotal*2, sizeof(REAL));
	hitAt10 = (REAL *)calloc(relationTotal*2, sizeof(REAL));
	hitAt3 = (REAL *)calloc(relationTotal*2, sizeof(REAL));
	hitAt1 = (REAL *)calloc(relationTotal*2, sizeof(REAL));
	memset(meanRank, 0, sizeof(REAL)*relationTotal*2);
	memset(meanRankReciprocal, 0, sizeof(REAL)*relationTotal*2);
	memset(hitAt10, 0, sizeof(REAL)*relationTotal*2);
	memset(hitAt3, 0, sizeof(REAL)*relationTotal*2);
	memset(hitAt1, 0, sizeof(REAL)*relationTotal*2);

	relationCount = (INT *)calloc(relationTotal*2, sizeof(INT));
	memset(relationCount, 0, sizeof(INT)*relationTotal*2);

    printf("All triples loaded.\n");
}

Triple *recommendList;

extern "C"
void importRecommendFiles() {
    printf("Start loading recommend file.\n");

    FILE *fin;
    INT tmp, recommendEntity; // recommendEntity: 0 = head given, 1 (or other) = tail given

	fin = fopen((inPath + "recommend2id.txt").c_str(), "r");
    tmp = fscanf(fin, "%ld", &recommendTotal);
    printf("Recommend total: %ld\n", recommendTotal);
    recommendList = (Triple *)calloc(recommendTotal, sizeof(Triple));

    for (INT i = 0; i < recommendTotal; i++) {
        tmp = fscanf(fin, "%ld", &recommendEntity);
        tmp = fscanf(fin, "%ld", &recommendList[i].r);
        if (recommendEntity == 0) {
            tmp = fscanf(fin, "%ld", &recommendList[i].h);
            recommendList[i].t = -1;
        } else {
            tmp = fscanf(fin, "%ld", &recommendList[i].t);
            recommendList[i].h = -1;
        }
        recommendList[i].w = 1.0;
    }

    fclose(fin);

    printf("Recommend file loaded.\n");
}

INT *head_lef;
INT *head_rig;
INT *tail_lef;
INT *tail_rig;
INT *head_type;
INT *tail_type;

extern "C"
void importTypeFiles() {
    printf("Start loading type constraint data.\n");
	INT total_lef = 0;
    INT total_rig = 0;
    FILE* f_type = fopen((inPath + "type_constrain.txt").c_str(),"r");
    INT tmp, rel, tot;
    tmp = fscanf(f_type, "%ld", &tmp);
    head_lef = (INT *)calloc(relationTotal, sizeof(INT));
    head_rig = (INT *)calloc(relationTotal, sizeof(INT));
    tail_lef = (INT *)calloc(relationTotal, sizeof(INT));
    tail_rig = (INT *)calloc(relationTotal, sizeof(INT));
    tmp = fscanf(f_type, "%ld", &tot);
    printf("Head total: %ld\t", tot);
    head_type = (INT *)calloc(tot, sizeof(INT));
    tmp = fscanf(f_type, "%ld", &tot);
    printf("Tail total: %ld\n", tot);
    tail_type = (INT *)calloc(tot, sizeof(INT));
    for (INT i = 0; i < relationTotal; i++) {
        tmp = fscanf(f_type, "%ld%ld", &rel, &tot);
        printf("Relation id: %ld\n", rel);
        head_lef[rel] = total_lef;
        for (INT j = 0; j < tot; j++) {
            tmp = fscanf(f_type, "%ld", &head_type[total_lef]);
            total_lef++;
        }
        head_rig[rel] = total_lef;
        // std::sort(head_type + head_lef[rel], head_type + head_rig[rel]);
        tmp = fscanf(f_type, "%ld%ld", &rel, &tot);
        tail_lef[rel] = total_rig;
        for (INT j = 0; j < tot; j++) {
            tmp = fscanf(f_type, "%ld", &tail_type[total_rig]);
            total_rig++;
        }
        tail_rig[rel] = total_rig;
        // std::sort(tail_type + tail_lef[rel], tail_type + tail_rig[rel]);
        printf("head_left: %ld head_right: %ld head_type_left:%ld head_type_right:%ld\n", head_lef[rel], head_rig[rel], head_type[head_lef[rel]], head_type[head_rig[rel]-1]);
        printf("tail_left: %ld tail_right: %ld tail_type_left:%ld tail_type_right:%ld\n", tail_lef[rel], tail_rig[rel], tail_type[tail_lef[rel]], tail_type[tail_rig[rel]-1]);
    }
    fclose(f_type);
    printf("All type constraint loaded.\n");
}


#endif
