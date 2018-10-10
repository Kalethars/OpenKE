#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=TransE --config=../config/TransE.config