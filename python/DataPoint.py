import numpy as np


class DataPoint:
    def __init__(self, position: np.ndarray, fitness: float):
        if not isinstance(position, np.ndarray):
            raise TypeError("position must be a numpy ndarray")
        if position.shape != (3,):
            raise ValueError("position must be a 3D numpy vector")

        self.position = position
        self.fitness = float(fitness)

    def __repr__(self):
        return f"DataPoint(position={self.position}, fitness={self.fitness})"
    
    def DataPoint(self, position: np.ndarray, fitness: float):
        return DataPoint(position, fitness)
