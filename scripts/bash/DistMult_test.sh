#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=DistMult --config=../config/DistMult_test.config --order=1
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=DistMult --config=../config/DistMult_test.config --order=2
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=DistMult --config=../config/DistMult_test.config --order=3
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=DistMult --config=../config/DistMult_test.config --order=4
python ../processor/result_analyzer.py --method=DistMult_test
python ../processor/result_recommendation.py --method=DistMult_test --unlimited=True
python ../processor/recommendation_analyzer --method=DistMult_test --unlimited=True
CUDA_VISIBLE_DEVICES="2" python ../kg_test.py --method=DistMult_test --weighted=True