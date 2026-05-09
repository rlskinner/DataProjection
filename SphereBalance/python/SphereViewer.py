import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as pgl
import OpenGL.GL as ogl


class SphereViewer:
    def __init__(self):
        pass

    # This method sets up the OpenGL view and displays a simple sphere.
    def run(self):
        app = pg.mkQApp("Sphere Points")
        w = pgl.GLViewWidget()
        w.show()
        w.setWindowTitle("Sphere Points")

        w.setCameraPosition(distance=10)

        axis = pgl.GLAxisItem()
        w.addItem(axis)
        w.addItem(SphereWireframeItem())  # Add the wireframe sphere to the view

        pg.exec()

class SphereWireframeItem(pgl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self,  parentItem: 'GLGraphicsItem' = None, latitude_steps=16, longitude_steps=8):
        super().__init__()
        self.sphereMesh = np.zeros((latitude_steps, longitude_steps, 3), dtype=np.float32)

        for i in range(latitude_steps):
            lat = np.radians(-90 + i * 180 / (latitude_steps - 1))
            for j in range(longitude_steps):
                lon = np.radians(j * 360 / longitude_steps)
                x = np.cos(lon) * np.sin(lat)
                y = np.sin(lon) * np.sin(lat)
                z = np.cos(lat)
                self.sphereMesh[i, j] = [x, y, z]


    def paint(self):
        ogl.glColor3f(0.0, 1.0, 1.0)  # cyan color

        # Draw latitude lines
        for i in range(self.sphereMesh.shape[0]):
            ogl.glBegin(ogl.GL_LINE_STRIP)
            for j in range(self.sphereMesh.shape[1]):
                ogl.glVertex3f(*self.sphereMesh[i, j])
            ogl.glVertex3f(*self.sphereMesh[i, 0])
            ogl.glEnd()

        # Draw longitude lines
        for j in range(self.sphereMesh.shape[1]):
            ogl.glBegin(ogl.GL_LINE_STRIP)
            for i in range(self.sphereMesh.shape[0]):
                ogl.glVertex3f(*self.sphereMesh[i, j])
            ogl.glVertex3f(*self.sphereMesh[0, j])
            ogl.glEnd()
        
        ogl.glFlush()


    

        
