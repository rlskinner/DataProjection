import json
import numpy as np

from SpherePointSet import SpherePointSet

class SphereBalancerConfig:
    def __init__(self):
        self.dict = {
            "balance_method": "equalize_fitness",
            "max_iterations": 100,
            "tolerance": 1e-5
        }

    def max_iterations(self):
        return self.dict.get("balance_method")
    
    def max_iterations(self):
        return self.dict.get("max_iterations")
    
    def tolerance(self):
        return self.dict.get("tolerance")

    # JSON serialization method
    def to_dict(self):
        return self.dict
    
    # Create SphereBalancerConfig from JSON string
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return SphereBalancerConfig.from_dict(data)
    
    # Create SphereBalancerConfig from JSON file
    @staticmethod
    def from_json_file(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return SphereBalancerConfig.from_dict(data)
    
    # JSON deserialization method
    @staticmethod
    def from_dict(data):
        cfg = SphereBalancerConfig()
        cfg.dict = {**cfg.dict, **data}
        return cfg
    
    # Method to save config to JSON string
    def to_json(self):
        return json.dumps(self.dict, indent=2)
    
    # Method to save config to JSON file
    def to_json_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.dict, f, indent=2) 


class SphereBalancer:
    def __init__(self, sphere_point_set, balancer_config):
        self.sphere_point_set = sphere_point_set
        if balancer_config is not None:
            self.cfg = balancer_config
        else:
            self.cfg = SphereBalancerConfig()


    def max_iterations(self):
        return self.cfg.max_iterations()
    
    def tolerance(self):
        return self.cfg.tolerance()
