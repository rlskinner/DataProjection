import numpy as np

from DataPoint import DataPoint

class DataSet:
    def __init__(self):
        self.data_points = []
        self.data_positions = {}



    def add_data_point(self, data_point):
        if not isinstance(data_point, DataPoint):
            raise TypeError("data_point must be an instance of DataPoint")
        
        if tuple(data_point.position) in self.data_positions:
            print(f"Duplicate DataPoint position, skipped: {data_point}")
            return
        
        self.data_points.append(data_point)
        self.data_positions[tuple(data_point.position)] = data_point.fitness

    def num_data_points(self):
        return len(self.data_points)

    def __repr__(self):
        return f"DataSet({len(self.data_points)} data points)"
    
    def get_data_point(self, index):
        if 0 <= index < len(self.data_points):
            return self.data_points[index]
        else:
            raise IndexError("Index out of bounds")
        
    