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

        w.setCameraPosition(distance=3.0)  # Set the camera distance to view the sphere

        axis = pgl.GLAxisItem()
        w.addItem(axis)

        wireframe = SphereWireframeItem(latitude_steps=9, longitude_steps=12)
        w.addItem(wireframe)

        pg.exec()

class SphereWireframeItem(pgl.GLGraphicsItem.GLGraphicsItem):
    def __init__(self,  parentItem: 'GLGraphicsItem' = None, latitude_steps=17, longitude_steps=4*9):
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


    

        
