#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBILE_DEVICE=0 python ../kg_train.py --method=TransE --config=../config/TransE_standalone.config