import numpy as np


class SpherePoint:
    def __init__(self, position: np.ndarray, fitness: float):
        if not isinstance(position, np.ndarray):
            raise TypeError("position must be a numpy ndarray")
        if position.shape != (3,):
            raise ValueError("position must be a 3D numpy vector")

        # Normalize positionto lie on the sphere
        norm = np.linalg.norm(position)
        if norm == 0:
            raise ValueError("position vector cannot be zero length")   
        self.position = position / norm
        self.fitness = float(fitness)

    def __repr__(self):
        return f"SpherePoint(position={self.position}, fitness={self.fitness})"
    
    def SpherePoint(self, position: np.ndarray, fitness: float):
        return SpherePoint(position, fitness)

    # JSON serialization method
    def to_dict(self):
        return {
            "position": self.position.tolist(),
            "fitness": self.fitness
        }
    
    # JSON deserialization method
    @staticmethod
    def from_dict(data):
        position = np.array(data["position"])
        fitness = float(data["fitness"])
        return SpherePoint(position, fitness)
    
    