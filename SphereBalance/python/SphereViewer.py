import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as pgl
import OpenGL.GL as ogl
from PyQt6.QtWidgets import QAbstractItemView, QWidget
from PyQt6.QtCore import QModelIndex, Qt, QRect, QPoint

from SpherePointSet import SpherePointSet


class SphereViewer(QAbstractItemView):
    def __init__(self, parent: QWidget|None=None, model=None, *args, **kwargs):
        super().__init__(*args, parent, **kwargs)
        
        self._model = None
        self._selected_indices = set()
        self._point_items = {}  # Maps model indices to GLScatterPlotItem
        
        self._glView = pgl.GLViewWidget(rotationMethod='euler')
        self._glView.setCameraPosition(distance=3.0)
        self._glView.show()        

        # Add coordinate axis
        axis = pgl.GLAxisItem()
        self._glView.addItem(axis)
        
        # Add sphere wireframe
        self._wireframe = SphereWireframeItem(latitude_steps=9, longitude_steps=12)
        self._glView.addItem(self._wireframe)
        
        if model:
            self.setModel(model)
    
    # QAbstractItemView required methods
    def setModel(self, model):
        """Set the model for this view"""
        if self._model:
            self._model.rowsInserted.disconnect(self._on_rows_inserted)
            self._model.rowsRemoved.disconnect(self._on_rows_removed)
            self._model.dataChanged.disconnect(self._on_data_changed)
            self._model.modelReset.disconnect(self._on_model_reset)
        
        self._model = model
        
        if model:
            model.rowsInserted.connect(self._on_rows_inserted)
            model.rowsRemoved.connect(self._on_rows_removed)
            model.dataChanged.connect(self._on_data_changed)
            model.modelReset.connect(self._on_model_reset)
            
            # Initial visualization
            self._refresh_view()
    
    def model(self):
        """Return the current model"""
        return self._model
    
    def visualRect(self, index):
        """Return the visual rect for a model index (always zero for 3D view)"""
        if not index.isValid():
            return QRect()
        return QRect()
    
    def scrollTo(self, index, hint=QAbstractItemView.ScrollHint.EnsureVisible):
        """Scroll to ensure index is visible (no-op for 3D view)"""
        pass
    
    def indexAt(self, point):
        """Get the model index at a screen point (ray casting in 3D)"""
        # For now, return invalid index - could be extended with ray casting
        return QModelIndex()
    
    def indexRegion(self, selection):
        """Get the region for a selection (no-op for 3D view)"""
        from PyQt6.QtGui import QRegion
        return QRegion()
    
    def horizontalOffset(self):
        """Return horizontal offset (not applicable for 3D)"""
        return 0
    
    def verticalOffset(self):
        """Return vertical offset (not applicable for 3D)"""
        return 0
    
    def isIndexHidden(self, index):
        """Check if index is hidden"""
        return False
    
    def moveCursor(self, cursorAction, modifiers):
        """Move cursor (not applicable for 3D)"""
        return QModelIndex()
    
    def setSelection(self, rect, command):
        """Set selection based on rect (simplified for 3D)"""
        pass
    
    # Model update handlers
    def _on_rows_inserted(self, parent, start, end):
        """Handle rows inserted in model"""
        if not self._model:
            return
        for row in range(start, end + 1):
            self._add_point_item(row)
    
    def _on_rows_removed(self, parent, start, end):
        """Handle rows removed from model"""
        for row in range(start, end + 1):
            self._remove_point_item(row)
    
    def _on_data_changed(self, topLeft, bottomRight, roles):
        """Handle data changed in model"""
        self._refresh_view()
    
    def _on_model_reset(self):
        """Handle model reset"""
        self._refresh_view()
    
    def _refresh_view(self):
        """Refresh the entire view from model"""
        if not self._model:
            return
        
        # Clear existing point items
        for item in self._point_items.values():
            self.removeItem(item)
        self._point_items.clear()
        
        # Add points from model
        for row in range(self._model.rowCount()):
            self._add_point_item(row)
    
    def _add_point_item(self, row):
        """Add a visual item for a point at the given row"""
        if not self._model:
            return
        
        point = self._model.get_data_point(row)
        
        # Create scatter plot item for this point
        positions = np.array([point.position], dtype=np.float32)
        size = 5
        color = (1.0, 0.0, 0.0, 1.0)  # Red by default
        
        scatter = pgl.GLScatterPlotItem(
            pos=positions,
            size=size,
            color=color,
            pxMode=False
        )
        
        self._glView.addItem(scatter)
        self._point_items[row] = scatter
    
    def _remove_point_item(self, row):
        """Remove the visual item for a point"""
        if row in self._point_items:
            self.removeItem(self._point_items[row])
            del self._point_items[row]
    


class SphereWireframeItem(pgl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self,  parentItem: 'pgl.GLGraphicsItem.GLGraphicsItem' = None, latitude_steps=17, longitude_steps=4*9):
        super().__init__()

        self.sphereMesh = np.zeros((latitude_steps, longitude_steps, 3), dtype=np.float32)
        for i in range(latitude_steps):
            lat = np.radians(i*180/(latitude_steps-1))
            for j in range(longitude_steps):
                lon = np.radians(j*360/longitude_steps)
                x = np.cos(lon) * np.sin(lat)
                y = np.sin(lon) * np.sin(lat)
                z = np.cos(lat)
                self.sphereMesh[i, j] = [x, y, z]

                # print(f"Vertex ({i}, {j}): {self.sphereMesh[i, j]}")
        pass

    def paint(self):
        # Old OpenGL code is deprecated!
        ogl.glMatrixMode(ogl.GL_MODELVIEW)
        ogl.glLoadMatrixf(self.modelViewMatrix().data())
        ogl.glMatrixMode(ogl.GL_PROJECTION)
        ogl.glLoadMatrixf(self.projectionMatrix().data())
        
        ogl.glColor3f(0.0, 1.0, 1.0)  # cyan color

        # Draw latitude lines
        for i in range(self.sphereMesh.shape[0]):
            ogl.glBegin(ogl.GL_LINE_LOOP)
            for j in range(self.sphereMesh.shape[1]):
                v = self.sphereMesh[i, j]
                ogl.glVertex3f(*self.sphereMesh[i, j])
            ogl.glEnd()

        # Draw longitude lines
        for j in range(self.sphereMesh.shape[1]):
            ogl.glBegin(ogl.GL_LINE_STRIP)
            for i in range(self.sphereMesh.shape[0]):
                v = self.sphereMesh[i, j]
                ogl.glVertex3f(*v)
            ogl.glEnd()
        
        self.update()


    

        
