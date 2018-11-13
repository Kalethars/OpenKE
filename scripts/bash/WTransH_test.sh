#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=WTransH --config=../config/WTransH_test.config --order=1
CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=WTransH --config=../config/WTransH_test.config --order=2
CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=WTransH --config=../config/WTransH_test.config --order=3