import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from thedatamine import hello_datamine

def main():
    hello_datamine()

if __name__ == '__main__':
    main()