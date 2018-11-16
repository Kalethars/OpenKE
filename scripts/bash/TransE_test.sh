#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=TransE --config=./config/TransE_test.config --order=1
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=TransE --config=./config/TransE_test.config --order=2
cd processor
python3 result_analyzer.py --method=TransE_test
python3 result_mapper.py --method=TransE_test --update=True
python3 result_recommendation.py --method=TransE_test --unlimited=True --update=True
python3 recommendation_analyzer --method=TransE_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=TransE_test --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=TransE_test --order=2 --weighted=True
