#!/usr/bin/env bash
python relation_combination.py --method=ComplEx_advanced --order=2 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=ComplEx_advanced --order=2 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=WComplEx_advanced --order=6 --predict=True --update=True --alg=maxmrr

python relation_combination.py --method=TransE_detailed --order=6 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=TransE_detailed --order=6 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=TransH_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=TransH_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=DistMult_detailed --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=DistMult_detailed --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=WTransH_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=WTransH_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=WTransE_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.05
python relation_combination.py --method=WTransE_test --order=1 --predict=True --update=True --alg=maxmrr --coeff=0.1

python relation_combination.py --method=WTransH_test --order=1 --predict=True --update=True --alg=maxmrr
python relation_combination.py --method=WTransE_test --order=1 --predict=True --update=True --alg=maxmrr