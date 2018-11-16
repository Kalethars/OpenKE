#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=1
cd processor
python3 result_analyzer.py --method=TransH_weighted
python3 result_mapper.py --method=TransH_weighted --update=True
python3 result_recommendation.py --method=TransH_weighted --unlimited=True --update=True
python3 recommendation_analyzer --method=TransH_weighted --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --weighted=True