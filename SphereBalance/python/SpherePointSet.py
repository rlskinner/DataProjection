import json
import numpy as np

from SpherePoint import SpherePoint

class SpherePointSet:
    def __init__(self, points):
        self.sphere_points = []
        self.sphere_positions = {}

        for point in points:
            self._add_data_point(point)

    # Internal method to add a data point, checks for duplicates
    def _add_data_point(self, data_point):
        if not isinstance(data_point, SpherePoint):
            raise TypeError("data_point must be an instance of SpherePoint")
        
        if tuple(data_point.position) in self.sphere_positions:
            print(f"Duplicate SpherePoint position, skipped: {data_point}")
            return
        
        self.sphere_points.append(data_point)
        self.sphere_positions[tuple(data_point.position)] = data_point.fitness

    def num_data_points(self):
        return len(self.sphere_points)

    def __repr__(self):
        return f"SpherePointSet({len(self.sphere_points)} data points)"
    
    def get_data_point(self, index):
        if 0 <= index < len(self.sphere_points):
            return self.sphere_points[index]
        else:
            raise IndexError("Index out of bounds")
        
    # To JSON string
    def to_json(self):
        return json.dumps(self.to_dict(), indent=2)
    
    # To JSON file
    def to_json_file(self, filename):
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    # Static method to create from JSON string
    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return SpherePointSet.from_dict(data)
    
    # Static method to create from JSON file
    @staticmethod
    def from_json_file(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        return SpherePointSet.from_dict(data)
    
    # JSON serialization method
    def to_dict(self):
        return {
            "sphere_points": [point.to_dict() for point in self.sphere_points]
        }

    # JSON deserialization method
    @staticmethod   
    def from_dict(data):
        points = [SpherePoint.from_dict(point_data) for point_data in data["sphere_points"]]
        return SpherePointSet(points)       
        
    