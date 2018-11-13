import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, required=True)
parsedArg = parser.parse_args()

f = open(parsedArg.file, 'w')
f.close()
