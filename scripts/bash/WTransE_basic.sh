#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=WTransE --config=../config/WTransE_basic.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=WTransE --config=../config/WTransE_basic.config --order=2
python ../processor/result_analyzer.py --method=WTransE_basic
python ../processor/result_recommendation.py --method=WTransE_basic --unlimited=True
python ../processor/recommendation_analyzer --method=WTransE_basic --unlimited=True
CUDA_VISIBLE_DEVICES="1" python ../kg_test.py --method=WTransE_basic --weighted=True