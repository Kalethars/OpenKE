#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_detailed.config --order=4
cd processor
python3 result_analyzer.py --method=DistMult_detailed
python3 result_mapper.py --method=DistMult_detailed --update=True
python3 result_recommendation.py --method=DistMult_detailed --unlimited=True --update=True
python3 recommendation_analyzer --method=DistMult_detailed --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_detailed --weighted=True