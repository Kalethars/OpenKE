#!/usr/bin/env bash
python kg_recommend.py --method=WTransE_test --order=1 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransE_test --order=1 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=WTransE_test --order=1
cd ..
cd processor
python relation_based_recommendation.py --method=WTransE_test --order=1
cd ..
python kg_recommend.py --method=TransH_test --order=1 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=TransH_test --order=1 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=TransH_test --order=1
cd ..
cd processor
python relation_based_recommendation.py --method=TransH_test --order=1
cd ..
python kg_recommend.py --method=WTransH_test --order=1 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WTransH_test --order=1 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=WTransH_test --order=1
cd ..
cd processor
python relation_based_recommendation.py --method=WTransH_test --order=1
cd ..
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=DistMult_detailed --order=1 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=DistMult_detailed --order=1
cd ..
cd processor
python relation_based_recommendation.py --method=DistMult_detailed --order=1
cd ..
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=ComplEx_advanced --order=2
cd ..
cd processor
python relation_based_recommendation.py --method=ComplEx_advanced --order=2
cd ..
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=0 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=0 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=1 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=1 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=2 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=2 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=3 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=3 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=4 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=4 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=5 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=5 --object=1 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=6 --object=0 --replace=1 --count=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=6 --object=1 --replace=1 --count=0
cd utils
python relation_distance_mapper.py --method=WComplEx_advanced --order=2
cd ..
cd processor
python relation_based_recommendation.py --method=WComplEx_advanced --order=2
cd ..
