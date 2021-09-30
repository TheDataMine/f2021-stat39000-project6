import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pandas as pd
from myproject.watch_data import WatchData

def main():
    print(f'Pandas is here!: {pd.__file__}')
    print(f'^^^^^^^')
    print(f'If that doesnt start with something like "$HOME/f2021-stat39000-project6/.venv/..., you did something wrong')
    
    dat = WatchData("/depot/datamine/apple/health/2021")
    print(dat)

if __name__ == '__main__':
    main()