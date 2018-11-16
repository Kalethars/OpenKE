#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=DistMult --config=./config/DistMult_test.config --order=1
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=DistMult --config=./config/DistMult_test.config --order=2
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=DistMult --config=./config/DistMult_test.config --order=3
CUDA_VISIBLE_DEVICES="2" python kg_train.py --method=DistMult --config=./config/DistMult_test.config --order=4
cd processor
python3 result_analyzer.py --method=DistMult_test
python3 result_mapper.py --method=DistMult_test --update=True
python3 result_recommendation.py --method=DistMult_test --unlimited=True --update=True
python3 recommendation_analyzer --method=DistMult_test --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=DistMult_test --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=DistMult_test --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=DistMult_test --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="2" python kg_test.py --method=DistMult_test --order=4 --weighted=True
