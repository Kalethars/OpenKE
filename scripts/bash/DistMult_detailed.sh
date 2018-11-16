#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=4
python ../processor/result_analyzer.py --method=DistMult_detailed
python ../processor/result_recommendation.py --method=DistMult_detailed --unlimited=True
python ../processor/recommendation_analyzer --method=DistMult_detailed --unlimited=True
CUDA_VISIBLE_DEVICES="1" python ../kg_test.py --method=DistMult_detailed --weighted=True