#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_detailed.config --order=8
