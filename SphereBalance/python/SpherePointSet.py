import json
import PyQt6
import numpy as np
import PyQt6.QtCore as QtCore

from SpherePoint import SpherePoint

class SpherePointSet(QtCore.QAbstractItemModel):
    def __init__(self, points):
        super().__init__()
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

    # QAbstractItemModel abstract methods
    def rowCount(self, parent=QtCore.QModelIndex()):
        """Return the number of rows (sphere points)"""
        if parent.isValid():
            return 0  # No children for flat list model
        return len(self.sphere_points)
    
    def columnCount(self, parent=QtCore.QModelIndex()):
        """Return the number of columns"""
        if parent.isValid():
            return 0
        return 5  # x, y, z, fitness, name
    
    def data(self, index, role=QtCore.Qt.ArrowType):
        """Return data for the given index and role"""
        if not index.isValid() or index.row() >= len(self.sphere_points):
            return None
        
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            point = self.sphere_points[index.row()]
            col = index.column()
            
            if col == 0:
                return f"{point.position[0]:.6f}"
            elif col == 1:
                return f"{point.position[1]:.6f}"
            elif col == 2:
                return f"{point.position[2]:.6f}"
            elif col == 3:
                return f"{point.fitness:.6f}"
            elif col == 4:
                return point.name if point.name else ""
        
        return None
    
    def headerData(self, section, orientation, role=QtCore.Qt.ItemDataRole.DisplayRole):
        """Return header data"""
        if role == QtCore.Qt.DisplayRole and orientation == QtCore.Qt.Horizontal:
            headers = ["X", "Y", "Z", "Fitness", "Name"]
            if 0 <= section < len(headers):
                return headers[section]
        
        return None
    
    def index(self, row, column, parent=QtCore.QModelIndex()):
        """Return the index for the given row and column"""
        if parent.isValid() or row < 0 or row >= len(self.sphere_points) or column < 0 or column >= 5:
            return QtCore.QModelIndex()
        
        return self.createIndex(row, column)
    
    def parent(self, index):
        """Return the parent index (always invalid for flat list)"""
        return PyQt6.QtCore.QModelIndex()

    def num_data_points(self):
        return len(self.sphere_points)

    def append_point(self, sphere_point):
        """Add a point to the model with proper signal emission"""
        if not isinstance(sphere_point, SpherePoint):
            raise TypeError("sphere_point must be an instance of SpherePoint")
        
        if tuple(sphere_point.position) in self.sphere_positions:
            print(f"Duplicate SpherePoint position, skipped: {sphere_point}")
            return
        
        row = len(self.sphere_points)
        self.beginInsertRows(PyQt6.QtCore.QModelIndex(), row, row)
        self.sphere_points.append(sphere_point)
        self.sphere_positions[tuple(sphere_point.position)] = sphere_point.fitness
        self.endInsertRows()
    
    def clear_points(self):
        """Clear all points from the model"""
        if self.sphere_points:
            self.beginRemoveRows(PyQt6.QtCore.QModelIndex(), 0, len(self.sphere_points) - 1)
            self.sphere_points.clear()
            self.sphere_positions.clear()
            self.endRemoveRows()

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
        
    