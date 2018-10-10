#!/usr/bin/env bash
CUDA_VISIBLE_DEVICES="0" python ../kg_train.py --method=TransE --config=../config/TransE_standalone.config