#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="0" python kg_train_new_relation.py --method=DistMult --config=./new_relation_config/DistMult_detailed.config --order=1
CUDA_VISIBLE_DEVICES="0" python kg_train_new_relation.py --method=DistMult --config=./new_relation_config/DistMult_detailed.config --order=2
CUDA_VISIBLE_DEVICES="0" python kg_train_new_relation.py --method=DistMult --config=./new_relation_config/DistMult_detailed.config --order=3
