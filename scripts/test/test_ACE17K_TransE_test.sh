#!/usr/bin/env bash
source ~/wangrj/tensorflow/bin/activate
python ../kg_test.py --database=ACE17K --method=TransE_test --order=1
python ../kg_test.py --database=ACE17K --method=TransE_test --order=2
