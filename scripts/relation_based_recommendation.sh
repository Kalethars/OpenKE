#!/usr/bin/env bash
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=3 --object=0 --replace=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=3 --object=1 --replace=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=0 --object=0 --replace=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=0 --object=1 --replace=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=5 --object=0 --replace=0
python kg_recommend.py --method=WComplEx_advanced --order=2 --relation=5 --object=1 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=3 --object=0 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=3 --object=1 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=0 --object=0 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=0 --object=1 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=5 --object=0 --replace=0
python kg_recommend.py --method=ComplEx_advanced --order=2 --relation=5 --object=1 --replace=0