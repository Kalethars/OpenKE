#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=8
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=9
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=10
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=11
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=12
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=13
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=14
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=15
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=KomplEx --config=./config/KomplEx_advanced.config --order=16
cd processor
python3 result_analyzer.py --method=KomplEx_advanced
python3 result_mapper.py --method=KomplEx_advanced --update=True
python3 result_recommendation.py --method=KomplEx_advanced --unlimited=True --update=True
python3 recommendation_analyzer --method=KomplEx_advanced --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=8 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=9 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=10 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=11 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=12 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=13 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=14 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=15 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=KomplEx_advanced --order=16 --weighted=True
cd processor
python3 result_analyzer.py --method=KomplEx_advanced --version=weighted
