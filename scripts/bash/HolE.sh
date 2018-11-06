#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=HolE --config=../config/HolE.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=HolE --config=../config/HolE.config --order=2
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=HolE --config=../config/HolE.config --order=3
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=HolE --config=../config/HolE.config --order=4
