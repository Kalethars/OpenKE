#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=TransE --config=../config/TransE_test.config --order=1
CUDA_VISIBLE_DEVICES="2" python ../kg_train.py --method=TransE --config=../config/TransE_test.config --order=2
