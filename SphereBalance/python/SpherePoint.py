import numpy as np


class SpherePoint:
    def __init__(self, position: np.ndarray, fitness: float):
        if not isinstance(position, np.ndarray):
            raise TypeError("position must be a numpy ndarray")
        if position.shape != (3,):
            raise ValueError("position must be a 3D numpy vector")

        self.position = position
        self.fitness = float(fitness)

    def __repr__(self):
        return f"SpherePoint(position={self.position}, fitness={self.fitness})"
    
    def SpherePoint(self, position: np.ndarray, fitness: float):
        return SpherePoint(position, fitness)
