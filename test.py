import os
import pandas as pd
import argparse

if __name__ == "__main__":
    csv = '../data/fantasy-football/1 - Introduction/epl_xg.csv'
    data = pd.read_csv(csv)
    print(data)