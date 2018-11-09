#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_weighted.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_weighted.config --order=2
