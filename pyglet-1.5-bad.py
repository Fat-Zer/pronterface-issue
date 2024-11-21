#!/usr/bin/env python

import os
import sys
from math import pi, sin, cos

import numpy
import wx
from wx import glcanvas

import pyglet
pyglet.options['debug_gl'] = True

from pyglet.gl import *

from pyglet import gl as pgl

def vec(*args):
    return (GLfloat * len(args))(*args)

class RootPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)

        box = wx.BoxSizer(wx.VERTICAL)
        box.Add((20, 30))
        btn = wx.Button(self, 0, "Add window")
        box.Add(btn, 0, wx.ALIGN_CENTER | wx.ALL, 15)
        self.Bind(wx.EVT_BUTTON, self.OnButton, btn)

        c = ConeCanvas(self)
        c.SetSize((200, 200))
        box.Add(c, 1, wx.EXPAND | wx.ALL, 15)

        self.SetAutoLayout(True)
        self.SetSizer(box)


    def OnButton(self, evt):
        frame = wx.Frame(None, wx.ID_ANY, "Cone", size=(400, 400))
        canvas = ConeCanvas(frame)
        frame.Show(True)


class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)

        # Initial mouse position.
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)


    def OnEraseBackground(self, event):
        pass  # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize() * self.GetContentScaleFactor()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, event):
        if self.HasCapture():
            self.ReleaseMouse()
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = event.GetPosition()

    def OnMouseUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnMouseMotion(self, event):
        if event.Dragging() and event.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = event.GetPosition()
            self.Refresh(False)

class ConeCanvas(MyCanvasBase):
    def InitGL( self ):
        self.pygletcontext = pgl.Context(pgl.current_context)
        self.pygletcontext.canvas = self
        self.pygletcontext.set_current()
        
        glMatrixMode(GL_PROJECTION)
        # Camera frustrum setup.
        glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
        glMaterialfv(GL_FRONT, GL_AMBIENT,  vec(0.2, 0.2, 0.2, 1.0))
        glMaterialfv(GL_FRONT, GL_DIFFUSE,  vec(0.8, 0.8, 0.8, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, vec(1.0, 0.0, 1.0, 1.0))
        glMaterialf(GL_FRONT, GL_SHININESS, 50.0)
        glLightfv(GL_LIGHT0, GL_AMBIENT,  vec(0.0, 1.0, 0.0, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  vec(1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))
        glLightfv(GL_LIGHT0, GL_POSITION, vec(1.0, 1.0, 1.0, 0.0))
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, vec(0.2, 0.2, 0.2, 1.0))
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Position viewer.
        glMatrixMode(GL_MODELVIEW)
        # Position viewer.
        glTranslatef(0.0, 0.0, -2.0);


    def OnDraw(self):
        # Clear color and depth buffers.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # Use a fresh transformation matrix.
        glPushMatrix()
        # Position object.
        ## glTranslatef(0.0, 0.0, -2.0)
        glRotatef(30.0, 1.0, 0.0, 0.0)
        glRotatef(30.0, 0.0, 1.0, 0.0)

        glTranslatef(0, -1, 0)
        glRotatef(250, 1, 0, 0)

        glEnable(GL_BLEND)
        glEnable(GL_POLYGON_SMOOTH)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 1.0, 0.5))
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 1.0)
        glShadeModel(GL_FLAT)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        # glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        base = .5
        height = 1.0
        slices = 16

        # Draw cone open ended without glu.
        tau = pi * 2
        glBegin(GL_TRIANGLE_FAN)
        centerX, centerY, centerZ = 0.0, 0.0, height
        glVertex3f(centerX, centerY, centerZ)  # Center of circle.
        centerX, centerY, centerZ = 0.0, 0.0, 0.0
        for i in range(slices + 1):
            theta = tau * float(i) / float(slices)  # Get the current angle.
            x = base * cos(theta)  # Calculate the x component.
            y = base * sin(theta)  # Calculate the y component.
            glVertex3f(x + centerX, y + centerY, centerZ)  # Output vertex.
        glEnd()

        glPopMatrix()
        glRotatef((self.y - self.lasty), 0.0, 0.0, 1.0);
        glRotatef((self.x - self.lastx), 1.0, 0.0, 0.0);
        # Push into visible buffer.
        self.SwapBuffers()

#----------------------------------------------------------------------

def main(argv):
    app = wx.App()
    frame = wx.Frame(None, title="GlCanvas demo", size=(200,400))
    RootPanel(frame)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    import sys
    main(sys.argv)

