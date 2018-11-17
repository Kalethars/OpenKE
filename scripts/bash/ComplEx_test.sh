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
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=17
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=18
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=19
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=20
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=21
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=22
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=23
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=24
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=25
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=26
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=27
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=28
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=29
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=30
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=31
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=32
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=33
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=34
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=35
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_test.config --order=36
cd processor
python3 result_analyzer.py --method=ComplEx_test
python3 result_mapper.py --method=ComplEx_test --update=True
python3 result_recommendation.py --method=ComplEx_test --unlimited=True --update=True
python3 recommendation_analyzer --method=ComplEx_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=8 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=9 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=10 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=11 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=12 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=13 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=14 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=15 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=16 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=17 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=18 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=19 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=20 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=21 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=22 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=23 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=24 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=25 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=26 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=27 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=28 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=29 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=30 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=31 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=32 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=33 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=34 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=35 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_test --order=36 --weighted=True
cd processor
python3 result_analyzer.py --method=ComplEx_test --version=weighted
