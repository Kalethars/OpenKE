#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=Analogy --config=./config/Analogy_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=Analogy --config=./config/Analogy_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=Analogy --config=./config/Analogy_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=Analogy --config=./config/Analogy_advanced.config --order=4
cd processor
python3 result_analyzer.py --method=Analogy_advanced
python3 result_mapper.py --method=Analogy_advanced --update=True
python3 result_recommendation.py --method=Analogy_advanced --unlimited=True --update=True
python3 recommendation_analyzer --method=Analogy_advanced --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=Analogy_advanced --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=Analogy_advanced --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=Analogy_advanced --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=Analogy_advanced --order=4 --weighted=True
cd processor
python3 result_analyzer.py --method=Analogy_advanced --version=weighted
