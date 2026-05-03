import json
import math
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

        # create scratch array of positions
        self.position_displacements = [np.zeros(3) for _ in range(self.sphere_point_set.num_data_points())]
        print("done")

        self.max_displacement = 0.0


    def max_iterations(self):
        return self.cfg.max_iterations()
    
    def tolerance(self):
        return self.cfg.tolerance()
    
    def next(self):
        # Implementation for the next balancing step

        # Initialize
        self.max_displacement = 0.0
        for i in range(len(self.position_displacements)):
            self.position_displacements[i].fill(0.0)

        for i in range(self.sphere_point_set.num_data_points()-1):
            for j in range(i+1, self.sphere_point_set.num_data_points()):
                self.find_displacements_to_balance_pair(i, j)

        # Scale the displacements and apply to the positions and normalize back to the sphere
        scale = 0.1  # This could be a parameter in the config
        for i in range(self.sphere_point_set.num_data_points()):
            displacement = self.position_displacements[i] * scale
            self.max_displacement = max(self.max_displacement, np.linalg.norm(displacement))
            self.sphere_point_set.get_data_point(i).position += displacement
            # Normalize the position back to the sphere
            self.sphere_point_set.get_data_point(i).position /= np.linalg.norm(self.sphere_point_set.get_data_point(i).position)
            print(f"new position for point {i}: {self.sphere_point_set.get_data_point(i).position}")
        
        return self.max_displacement > self.tolerance() 

    def find_displacements_to_balance_pair(self, i, j):
        p_i = self.sphere_point_set.get_data_point(i)
        p_j = self.sphere_point_set.get_data_point(j)

        # Angle (arc length) between the points -> displacement arc length
        arc_length = np.arccos(np.clip(np.dot(p_i.position, p_j.position), -1.0, 1.0))
        arc_displacement = (math.pi - arc_length) / 2
        # print(f"arc_length: {arc_length}")
        # print(f"arc_displacement: {arc_displacement}")  

        # Normal vector p_i x p_j
        p_i_j_normal = np.cross(p_i.position, p_j.position)
        p_i_j_normal /= np.linalg.norm(p_i_j_normal)
        # print(f"normalized p_i_j_normal: {p_i_j_normal}")

        # The i and j displacement directions are perpindicular to the normal vector
        p_i_displacement_direction = np.cross(p_i.position, p_i_j_normal)
        p_j_displacement_direction = np.cross(p_i_j_normal, p_j.position)
        # print(f"p_i_displacement_direction: {p_i_displacement_direction}")
        # print(f"p_j_displacement_direction: {p_j_displacement_direction}")  

        # The displacement directions are normal vectors,
        # so the displacements are scaled by the arc displacement
        p_i_displacement = arc_displacement * p_i_displacement_direction
        p_j_displacement = arc_displacement * p_j_displacement_direction
        # print(f"p_i_displacement: {p_i_displacement}")
        # print(f"p_j_displacement: {p_j_displacement}")

        # Accumulate the pairwise displacements
        self.position_displacements[i] += p_i_displacement
        self.position_displacements[j] += p_j_displacement
        

        # # Interesting.  The following was auto-suggested.  
        # # Compute the difference in fitness
        # fitness_diff = p_i.fitness - p_j.fitness

        # # Compute the direction vector from p_i to p_j
        # direction = p_j.position - p_i.position
        # distance = np.linalg.norm(direction)u

        # if distance > 0:
            # # Normalize the direction vector
            # direction /= distance

            # # Compute the movement based on fitness difference and distance
            # movement = self.cfg.tolerance() * fitness_diff / (distance + 1e-8)  # Add small value to avoid division by zero

            # # Update scratch positions
            # self.scratch_positions[i] += movement * direction
            # self.scratch_positions[j] -= movement * direction

            # # Track maximum movement for convergence check
            # self.max_movement = max(self.max_movement, abs(movement)) # Return False when balancing is complete
        
