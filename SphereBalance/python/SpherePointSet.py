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
        
    