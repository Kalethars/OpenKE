#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransE --config=./config/TransE_weighted.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransE --config=./config/TransE_weighted.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransE --config=./config/TransE_weighted.config --order=3
cd processor
python3 result_analyzer.py --method=TransE_weighted
python3 result_mapper.py --method=TransE_weighted --update=True
python3 result_recommendation.py --method=TransE_weighted --unlimited=True --update=True
python3 recommendation_analyzer --method=TransE_weighted --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransE_weighted --weighted=True