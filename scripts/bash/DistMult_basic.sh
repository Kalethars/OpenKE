#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=1
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=2
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=3
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=4
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=5
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=6
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=7
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=8
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=9
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=10
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=11
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=12
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=13
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=14
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=15
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=16
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=17
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=18
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=19
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=20
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=21
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=22
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=23
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=24
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=25
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=26
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=27
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=28
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=29
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=30
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=31
CUDA_VISIBLE_DEVICES="1" python kg_train.py --method=DistMult --config=./config/DistMult_basic.config --order=32
cd processor
python3 result_analyzer.py --method=DistMult_basic
python3 result_mapper.py --method=DistMult_basic --update=True
python3 result_recommendation.py --method=DistMult_basic --unlimited=True --update=True
python3 recommendation_analyzer --method=DistMult_basic --unlimited=True
cd ..
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=1 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=2 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=3 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=4 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=5 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=6 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=7 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=8 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=9 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=10 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=11 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=12 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=13 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=14 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=15 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=16 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=17 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=18 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=19 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=20 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=21 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=22 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=23 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=24 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=25 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=26 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=27 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=28 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=29 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=30 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=31 --weighted=True
CUDA_VISIBLE_DEVICES="1" python kg_test.py --method=DistMult_basic --order=32 --weighted=True
