#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WTransE --config=./config/WTransE_basic.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WTransE --config=./config/WTransE_basic.config --order=2
cd processor
python3 result_analyzer.py --method=WTransE_basic
python3 result_mapper.py --method=WTransE_basic --update=True
python3 result_recommendation.py --method=WTransE_basic --unlimited=True --update=True
python3 recommendation_analyzer --method=WTransE_basic --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WTransE_basic --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WTransE_basic --order=2 --weighted=True
cd processor
python3 result_analyzer.py --method=WTransE_basic --version=weighted
