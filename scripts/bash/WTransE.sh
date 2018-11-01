#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --weighted=True --config=../config/WTransE.config --order=1
