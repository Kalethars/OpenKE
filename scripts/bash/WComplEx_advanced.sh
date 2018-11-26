#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=8
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=9
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=10
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=11
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=12
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=13
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=14
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=15
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=16
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=17
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=18
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=19
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=20
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=21
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=22
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=23
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=24
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=25
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=26
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=27
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=28
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=29
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=30
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=31
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=WComplEx --config=./config/WComplEx_advanced.config --order=32
cd processor
python3 result_analyzer.py --method=WComplEx_advanced
python3 result_mapper.py --method=WComplEx_advanced --update=True
python3 result_recommendation.py --method=WComplEx_advanced --unlimited=True --update=True
python3 recommendation_analyzer --method=WComplEx_advanced --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=8 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=9 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=10 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=11 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=12 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=13 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=14 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=15 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=16 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=17 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=18 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=19 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=20 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=21 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=22 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=23 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=24 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=25 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=26 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=27 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=28 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=29 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=30 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=31 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=WComplEx_advanced --order=32 --weighted=True
cd processor
python3 result_analyzer.py --method=WComplEx_advanced --version=weighted
