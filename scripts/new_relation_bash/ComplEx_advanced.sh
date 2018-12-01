#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=8
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=9
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=10
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=11
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=12
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=13
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=14
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=15
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=ComplEx --config=./new_relation_config/ComplEx_advanced.config --order=16
