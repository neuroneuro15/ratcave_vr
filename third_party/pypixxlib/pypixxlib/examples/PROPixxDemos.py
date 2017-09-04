from math import cos
from math import pi
from math import sin
import time
from pypixxlib.propixx import PROPixx
from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PySide import QtOpenGL, QtGui
from PySide.QtCore import QTimer
from PySide.QtGui import QMainWindow, QApplication
from PySide.QtGui import QPixmap
from PySide.QtOpenGL import QGLWidget


def override(interface_class):
    def override(method):
        assert(method.__name__ in dir(interface_class))
        return method
    return override


class proPixx480_1440test(QtOpenGL.QGLWidget):
    """
    This class is a custom QGLWidget.
    
    Functions:
        - initializeGL(self) (overridden):
                What runs when the widget is created.
        - paintGL(self) (overridden): 
                Runs every time an update is requested.
    """
                
    def __init__(self, parent=None):
        QtOpenGL.QGLWidget.__init__(self, parent)
        """
        Initializes the OpenGl widget.
        
        Attributes:
            - Parent
            
        Return:
            - NA
        
        """
        self.red = 0
        self.green = 0
        self.blue = 0
        self.width = 1920
        self.height = 50
        self.quad_w = 255
        self.time = 0
        self.frame_number = 0
        self.mode = 0
        
    
    def initializeGL(self):
        """
        Initializes the OpenGl Pipeline.  glViewport values are based on the VIEWPixx settings.
        The color height is fixed valued chosen because it looks nice.
        
        Attributes:
            - self
            
        Return:
            - NA
        
        """
        self.time = time.time()

        
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GL.glOrtho( 0, 1920, 0, 1080, 0, 1)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        GL.glClearColor(0.0, 0.0, 0.0, 0.0)
        GL.glDisable(GL.GL_DITHER)
         
  
    def paintGL(self):
        """ Seperate the screen in 4 QUADS for appropriate 480/1440 Hz display"""
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        
        if self.mode is 0:
            GL.glViewport(0, 540, 960, 540) # QUAD 1
            GL.glBegin(GL.GL_POLYGON)
            GL.glColor3ub(255, 0, 0)
            sides = 32
            radius = 120  
            glVertex2f(1920/2, 1080/2)
            for i in range(sides - sides/8 + 1):
                cosine= radius * cos(i*2*pi/sides+2*pi*(self.frame_number % 25 + 0)/25) + 1920/2
                sine  = radius * sin(i*2*pi/sides+2*pi*(self.frame_number % 25 + 0)/25) + 1080/2
                glVertex2f(cosine,sine)
            GL.glEnd()
            
            
            GL.glViewport(960, 540, 960, 540) # QUAD 2
            GL.glBegin(GL.GL_POLYGON)
            GL.glColor3ub(0, 255, 0)
            sides = 32
            radius = 120  
            glVertex2f(1920/2, 1080/2)
            for i in range(sides - sides/8 + 1):
                cosine= radius * cos(i*2*pi/sides+2*pi*(self.frame_number % 25 + 1)/25) + 1920/2
                sine  = radius * sin(i*2*pi/sides+2*pi*(self.frame_number % 25 + 1)/25) + 1080/2
                glVertex2f(cosine,sine)
            GL.glEnd()
            
            GL.glViewport(0, 0, 960, 540) # QUAD 3
            GL.glBegin(GL.GL_POLYGON)
            GL.glColor3ub(0, 0, 255)
            sides = 32
            radius = 120  
            glVertex2f(1920/2, 1080/2)
            for i in range(sides - sides/8 + 1):
                cosine= radius * cos(i*2*pi/sides+2*pi*(self.frame_number % 25 + 2)/25) + 1920/2
                sine  = radius * sin(i*2*pi/sides+2*pi*(self.frame_number % 25 + 2)/25) + 1080/2
                glVertex2f(cosine,sine)
            GL.glEnd()        
            
            GL.glViewport(960, 0, 960, 540) # QUAD 4
            GL.glBegin(GL.GL_POLYGON)
            GL.glColor3ub(0, 0, 0)
            sides = 32
            radius = 120  
            glVertex2f(1920/2, 1080/2)
            for i in range(sides - sides/8 + 1):
                cosine= radius * cos(i*2*pi/sides+2*pi*(self.frame_number % 25 + 3)/25) + 1920/2
                sine  = radius * sin(i*2*pi/sides+2*pi*(self.frame_number % 25 + 3)/25) + 1080/2
                glVertex2f(cosine,sine)
            GL.glEnd()        
      
      
        if self.mode is 1:
            
            GL.glViewport(0, 540, 960, 540) # QUAD 1
            self.speed = 1
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 0) % 1080, 10, 255, 0, 0) # R1
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 20) % 1080, 10, 0, 255, 0) # G1
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 40) % 1080, 10, 0, 0, 255) # B1
            
            GL.glViewport(960, 540, 960, 540) # QUAD 2
    
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 5) % 1080, 10, 255, 0, 0) # R2
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 25) % 1080, 10, 0, 255, 0) # G2
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 45) % 1080, 10, 0, 0, 255) # B2            
            
            GL.glViewport(0, 0, 960, 540) # QUAD 3

            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 10) % 1080, 10, 255, 0, 0) # R3
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 30) % 1080, 10, 0, 255, 0) # G3
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 50) % 1080, 10, 0, 0, 255) # B3     
            
            GL.glViewport(960, 0, 960, 540) # QUAD 4
     
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 15) % 1080, 10, 255, 0, 0) # R4
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 35) % 1080, 10, 0, 255, 0) # G4
            self.genQuads(1920/2-50, (12*(self.frame_number % 1080) + 55) % 1080, 10, 0, 0, 255) # B4    
        
        
        self.frame_number += 1
        #print (time.time() - self.time)*1000
        self.time = time.time()
        
    def genQuads(self, x, y, size, r, g, b,):
        GL.glBegin(GL.GL_QUADS)
        GL.glColor3ub(r, g, b)
        GL.glVertex2i(x, y)
        GL.glVertex2i(x, y+size)
        GL.glVertex2i(x+size, y+size)
        GL.glVertex2i(x+size, y)
        GL.glEnd() 
 
class demo(QApplication):
    "Simple application for testing OpenGL rendering"
    def __init__(self, number=1):
        QApplication.__init__(self, sys.argv)
        self.setApplicationName("SphereTest")
        self.mainWindow = QMainWindow()
        self.gl_widget = proPixx480_1440test()
        self.mainWindow.setCentralWidget(self.gl_widget)
        self.mainWindow.setGeometry(QtGui.QDesktopWidget().availableGeometry(1))
        self.mainWindow.showFullScreen()
        self.curr_time = time.time()
        self.timer = QTimer()
        self.timer.setInterval(0)
        self.timer.timeout.connect(self.gl_widget.update)
        self.timer.start()
        self.timer2 = QTimer()
        self.timer2.setInterval(3000)
        self.timer2.timeout.connect(self.printFrames)
        self.timer2.start()
        self.gl_widget.mode = number
        self.gl_widget.mouseDoubleClickEvent = lambda x : self.mainWindow.close()
        self.previous_time = 0
        self.previous_total = 0

        my_device = PROPixx()
        if number is 0: # 480 Hz
            my_device.setDlpSequencerProgram('QUAD4X')
        else: # 1440 Hz
            my_device.setDlpSequencerProgram('QUAD12X')
        my_device.updateRegisterCache()
        
        sys.exit(self.exec_()) # Start Qt main loop

    def printFrames(self):
        
        time_ela =  self.gl_widget.time - self.curr_time
        new_time = time_ela - self.previous_time
        self.previous_time = time_ela
        new_frames = self.gl_widget.frame_number - self.previous_total
        self.previous_total = self.gl_widget.frame_number
        print "There have been %d frames in %f seconds, so %f FPS" %  (new_frames, new_time, new_frames/float(new_time))

if __name__ == "__main__":
    demo(1)
    