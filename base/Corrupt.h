#ifndef CORRUPT_H
#define CORRUPT_H
#include "Random.h"
#include "Triple.h"
#include "Reader.h"

bool _find(INT h, INT t, INT r) {
    INT lef = 0;
    INT rig = tripleTotal - 1;
    INT mid;
    while (lef + 1 < rig) {
        INT mid = (lef + rig) >> 1;
        if ((tripleList[mid]. h < h) || (tripleList[mid]. h == h && tripleList[mid]. r < r) || (tripleList[mid]. h == h && tripleList[mid]. r == r && tripleList[mid]. t < t)) lef = mid; else rig = mid;
    }
    if (tripleList[lef].h == h && tripleList[lef].r == r && tripleList[lef].t == t) return true;
    if (tripleList[rig].h == h && tripleList[rig].r == r && tripleListcd [rig].t == t) return true;
    return false;
}


INT corrupt_head(INT id, INT t, INT r) {
    while (true) {
        INT h = head_type[rand_max(id, head_rig[r] - head_lef[r]) + head_lef[r]];
        if (not _find(h, t, r)) {
            return h;
        }
    }
}


INT corrupt_tail(INT id, INT h, INT r) {
    while (true) {
        INT t = tail_type[rand_max(id, tail_rig[r] - tail_lef[r]) + tail_lef[r]];
        if (not _find(h, t, r)) {
            return t;
        }
    }
}


INT corrupt_rel(INT id, INT h, INT t) {
	INT lef, rig, mid, ll, rr;
	lef = lefRel[h] - 1;
	rig = rigRel[h];
	while (lef + 1 < rig) {
		mid = (lef + rig) >> 1;
		if (trainRel[mid].t >= t) rig = mid; else
		lef = mid;
	}
	ll = rig;
	lef = lefRel[h];
	rig = rigRel[h] + 1;
	while (lef + 1 < rig) {
		mid = (lef + rig) >> 1;
		if (trainRel[mid].t <= t) lef = mid; else
		rig = mid;
	}
	rr = lef;
	INT tmp = rand_max(id, relationTotal - (rr - ll + 1));
	if (tmp < trainRel[ll].r) return tmp;
	if (tmp > trainRel[rr].r - rr + ll - 1) return tmp + rr - ll + 1;
	lef = ll, rig = rr + 1;
	while (lef + 1 < rig) {
		mid = (lef + rig) >> 1;
		if (trainRel[mid].r - mid + ll - 1 < tmp)
			lef = mid;
		else 
			rig = mid;
	}
	return tmp + lef - ll + 1;
}


INT corrupt(INT h, INT r){
	INT ll = tail_lef[r];
	INT rr = tail_rig[r];
	INT loop = 0;
	INT t;
	while(1) {
		t = tail_type[rand(ll, rr)];
		if (not _find(h, t, r)) {
		//	printf("r:%ld\tt:%ld\n", r, t);
			return t;
		} else {
			loop ++;
			if (loop >= 1000){
			//	printf("drop\n");
				return corrupt_head(0, h, r);
			}
		} 
	}
}
#endif
