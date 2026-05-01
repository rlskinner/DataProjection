import argparse
import numpy as np
import json

from SpherePoint import SpherePoint
from SpherePointSet import SpherePointSet


def parse_args():
    parser = argparse.ArgumentParser(description="Process a filename and optional projection config.")
    parser.add_argument("filename", help="Path to the input file")
    parser.add_argument(
        "--proj",
        dest="projectionConfig",
        help="Path to a projection configuration file (optional)",
        default=None,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load the data set from the specified JSON file 
    ds = SpherePointSet.from_json_file(args.filename)
    print("Initial data set:") 
    print(ds.to_json())

if __name__ == "__main__":
    main()
