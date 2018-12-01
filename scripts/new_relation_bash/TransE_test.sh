#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_test.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_test.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train_new_relation.py --method=TransE --config=./new_relation_config/TransE_test.config --order=3
