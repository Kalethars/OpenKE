#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_detailed.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_detailed.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_detailed.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=ComplEx --config=./config/ComplEx_detailed.config --order=4
cd processor
python3 result_analyzer.py --method=ComplEx_detailed
python3 result_mapper.py --method=ComplEx_detailed --update=True
python3 result_recommendation.py --method=ComplEx_detailed --unlimited=True --update=True
python3 recommendation_analyzer --method=ComplEx_detailed --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_detailed --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_detailed --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_detailed --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=ComplEx_detailed --order=4 --weighted=True
