#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=DistMult --config=../config/DistMult_detailed.config --order=4
