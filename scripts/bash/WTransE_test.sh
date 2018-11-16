#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WTransE --config=./config/WTransE_test.config --order=1
cd processor
python3 result_analyzer.py --method=WTransE_test
python3 result_mapper.py --method=WTransE_test --update=True
python3 result_recommendation.py --method=WTransE_test --unlimited=True --update=True
python3 recommendation_analyzer --method=WTransE_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WTransE_test --order=1 --weighted=True
cd processor
python3 result_analyzer.py --method=WTransE_test --version=weighted
