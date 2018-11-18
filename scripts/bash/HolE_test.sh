#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=HolE --config=./config/HolE_test.config --order=8
cd processor
python3 result_analyzer.py --method=HolE_test
python3 result_mapper.py --method=HolE_test --update=True
python3 result_recommendation.py --method=HolE_test --unlimited=True --update=True
python3 recommendation_analyzer --method=HolE_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=HolE_test --order=8 --weighted=True
cd processor
python3 result_analyzer.py --method=HolE_test --version=weighted
