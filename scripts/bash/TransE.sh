#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=1
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=2
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=3
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=4
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=5
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=6
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=7
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=8
CUDA_VISIBLE_DEVICES="0,1,2,3" python ../kg_train.py --method=TransE --config=../config/TransE.config --order=9
