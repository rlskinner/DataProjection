import argparse
import numpy as np

from DataPoint import DataPoint
from DataSet import DataSet


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
    print(f"Filename: {args.filename}")
    if args.projectionConfig is not None:
        print(f"Projection config: {args.projectionConfig}")

    ds = DataSet()
    print(ds)
    ds.add_data_point(DataPoint(np.array([1.0, 2.0, 3.0]), 0.5))
    ds.add_data_point(DataPoint(np.array([3.0, 4.0, 5.0]), 0.75))
    ds.add_data_point(DataPoint(np.array([3.0, 4.0, 5.0]), 0.25))
    print(ds)
    

if __name__ == "__main__":
    main()
