#!/usr/bin/env bash
python relation_combination.py --method=TransH_test --order=1 --predict=True --update=True --alg=mindist
python relation_combination.py --method=ComplEx_advanced --order=2 --predict=True --update=True --alg=mindist

python relation_combination.py --method=WTransH_test --order=1 --predict=True --update=True --alg=mindist --coeff=0.05
python relation_combination.py --method=WTransH_test --order=1 --predict=True --update=True --alg=mindist --coeff=0.1

python relation_combination.py --method=WTransE_test --order=1 --predict=True --update=True --alg=mindist --coeff=0.05
python relation_combination.py --method=WTransE_test --order=1 --predict=True --update=True --alg=mindist --coeff=0.1