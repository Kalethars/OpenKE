#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_test.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_test.config --order=2
cd processor
python3 result_analyzer.py --method=TransH_test
python3 result_mapper.py --method=TransH_test --update=True
python3 result_recommendation.py --method=TransH_test --unlimited=True --update=True
python3 recommendation_analyzer --method=TransH_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_test --weighted=True