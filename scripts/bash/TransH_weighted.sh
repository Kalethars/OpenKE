#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransH --config=../config/TransH_weighted.config --order=1
