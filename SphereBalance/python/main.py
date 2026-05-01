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
    print(f"Filename: {args.filename}")
    if args.projectionConfig is not None:
        print(f"Projection config: {args.projectionConfig}")

    points = [
        SpherePoint(np.array([1.0, 2.0, 3.0]), 0.5),
        SpherePoint(np.array([3.0, 4.0, 5.0]), 0.75),
        SpherePoint(np.array([3.0, 4.0, 5.0]), 0.25),
    ]
    ds = SpherePointSet(points)
    print(ds)
    
    # Test JSON serialization
    ds_json = ds.to_json()
    print("Serialized SpherePointSet to JSON:")
    print(ds_json)

    # Test JSON deserialization 
    ds_from_json = SpherePointSet.from_json_file(args.filename)
    print("Deserialized SpherePointSet from JSON:") 
    print(ds_from_json.to_json())

if __name__ == "__main__":
    main()
