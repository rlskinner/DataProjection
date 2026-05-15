import argparse
import numpy as np
import json
import pyqtgraph as pg

from SpherePoint import SpherePoint
from SpherePointSet import SpherePointSet
from SphereBalancer import SphereBalancer, SphereBalancerConfig
from SphereViewer import SphereViewer

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

    # Load data set from the specified JSON file 
    ds = SpherePointSet.from_json_file(args.filename)

    balancer_config = SphereBalancerConfig()
    if args.balancerConfigPath is not None:
        balancer_config = SphereBalancerConfig.from_json_file(args.balancerConfigPath)
    # print("Configured balancer")
    # print(balancer.to_json())

    balancer = SphereBalancer(balancer_config)

    # while balancer.next():
        # pass
   
    """Run the viewer as a standalone application"""
    app = pg.mkQApp("Sphere Points")
    sv = SphereViewer()
    sv.setModel(ds)
    sv.setBalancer(balancer)

    app.exec()
    
if __name__ == "__main__":
    main()
