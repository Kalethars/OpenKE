#!/usr/bin/env bash
python fieldPaper_analyzer.py --method=WComplEx_advanced --order=6
python fieldPaper_analyzer.py --method=ComplEx_advanced --order=2
python fieldPaper_analyzer.py --method=WTransH_test --order=1
python fieldPaper_analyzer.py --method=TransH_test --order=1
python fieldPaper_analyzer.py --method=WTransE_test --order=1
python fieldPaper_analyzer.py --method=TransE_detailed --order=6
python fieldPaper_analyzer.py --method=DistMult_detailed --order=1
