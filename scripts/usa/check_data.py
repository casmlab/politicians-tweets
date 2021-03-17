import json
import pandas as pd
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser()        
    parser.add_argument('--corpus_file', type=str,help="The file name for the text file to use in training")

    args = parser.parse_args()
    if not args.corpus_file:
        print('No file specified for training! See help message:\n')
        parser.print_help(sys.stderr)
        exit(1)
    corpus_file_name = args.corpus_file
    df = pd.read_json(corpus_file_name)
    print('Number of accounts being pulled: %d'%df.screen_name.nunique())

