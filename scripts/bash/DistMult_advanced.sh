#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=4
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=5
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=6
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=7
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_advanced.config --order=8
python ../processor/result_analyzer.py --method=DistMult_advanced
python ../processor/result_recommendation.py --method=DistMult_advanced --unlimited=True
python ../processor/recommendation_analyzer --method=DistMult_advanced --unlimited=True
CUDA_VISIBLE_DEVICES="1" python ../kg_test.py --method=DistMult_advanced --weighted=True