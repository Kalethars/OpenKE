#!/usr/bin/env bash
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=6 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=WComplEx_advanced --order=6
cd ..
cd processor
python relation_based_recommendation.py --method=WComplEx_advanced --order=6
cd ..
