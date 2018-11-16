#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=WTransE --config=../config/WTransE_test.config --order=1
python ../processor/result_analyzer.py --method=WTransE_test
python ../processor/result_recommendation.py --method=WTransE_test --unlimited=True
python ../processor/recommendation_analyzer --method=WTransE_test --unlimited=True
CUDA_VISIBLE_DEVICES="1" python ../kg_test.py --method=WTransE_test --weighted=True