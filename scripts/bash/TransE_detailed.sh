#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=4
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=5
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=6
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=7
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=8
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=9
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=10
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=11
CUDA_VISIBLE_DEVICES="1" python ../kg_train.py --method=TransE --config=../config/TransE_detailed.config --order=12
