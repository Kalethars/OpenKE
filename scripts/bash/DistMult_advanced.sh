#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_advanced.config --order=8
cd processor
python3 result_analyzer.py --method=DistMult_advanced
python3 result_mapper.py --method=DistMult_advanced --update=True
python3 result_recommendation.py --method=DistMult_advanced --unlimited=True --update=True
python3 recommendation_analyzer --method=DistMult_advanced --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_advanced --order=8 --weighted=True
cd processor
python3 result_analyzer.py --method=DistMult_advanced --version=weighted
