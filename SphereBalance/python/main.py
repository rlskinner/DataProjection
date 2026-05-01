import argparse
import numpy as np
import json

from SpherePoint import SpherePoint
from SpherePointSet import SpherePointSet
from SphereBalancer import SphereBalancer, SphereBalancerConfig


def parse_args():
    parser = argparse.ArgumentParser(description="Process a filename and optional balancer config.")
    parser.add_argument("filename", help="Path to the input file")
    parser.add_argument(
        "--balancer",
        dest="balancerConfigPath",
        help="Path to a balancer configuration file (optional)",
        default=None,
    )
    return parser.parse_args()


def main():
    args = parse_args()

    balancer = SphereBalancerConfig()
    print("default balancer")
    print(balancer.to_json())
    print(f"tolerance: {balancer.tolerance()}")

    if args.balancerConfigPath is not None:
        balancer = SphereBalancerConfig.from_json_file(args.balancerConfigPath)
        print("Configured balancer")
        print(balancer.to_json())
        print(f"tolerance: {balancer.tolerance()}")

    # Load the data set from the specified JSON file 
    ds = SpherePointSet.from_json_file(args.filename)
    print("Initial data set:") 
    print(ds.to_json())

if __name__ == "__main__":
    main()
