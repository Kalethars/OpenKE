#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=TransH --config=./config/TransH_weighted.config --order=8
cd processor
python3 result_analyzer.py --method=TransH_weighted
python3 result_mapper.py --method=TransH_weighted --update=True
python3 result_recommendation.py --method=TransH_weighted --unlimited=True --update=True
python3 recommendation_analyzer --method=TransH_weighted --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=TransH_weighted --order=8 --weighted=True
cd processor
python3 result_analyzer.py --method=TransH_weighted --version=weighted
