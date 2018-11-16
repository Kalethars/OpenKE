#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=8
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=9
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=10
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=11
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=12
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=13
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=14
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=15
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=16
cd processor
python3 result_analyzer.py --method=ComplEx_test
python3 result_mapper.py --method=ComplEx_test --update=True
python3 result_recommendation.py --method=ComplEx_test --unlimited=True --update=True
python3 recommendation_analyzer --method=ComplEx_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --weighted=True