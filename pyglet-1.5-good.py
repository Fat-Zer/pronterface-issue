#!/usr/bin/env python

import os
import sys
from math import pi, sin, cos

import numpy
import wx
from wx import glcanvas

import pyglet
pyglet.options['debug_gl'] = True

from pyglet import gl

def vec(*args):
    return (gl.GLfloat * len(args))(*args)

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
        gl.glViewport(0, 0, size.width, size.height)

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
        self.pygletcontext = gl.Context(gl.current_context)
        self.pygletcontext.canvas = self
        self.pygletcontext.set_current()
        
        gl.glMatrixMode(gl.GL_PROJECTION)
        # Camera frustrum setup.
        gl.glFrustum(-0.5, 0.5, -0.5, 0.5, 1.0, 3.0)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT,  vec(0.2, 0.2, 0.2, 1.0))
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_DIFFUSE,  vec(0.8, 0.8, 0.8, 1.0))
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_SPECULAR, vec(1.0, 0.0, 1.0, 1.0))
        gl.glMaterialf(gl.GL_FRONT, gl.GL_SHININESS, 50.0)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_AMBIENT,  vec(0.0, 1.0, 0.0, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE,  vec(1.0, 1.0, 1.0, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, vec(1.0, 1.0, 1.0, 0.0))
        gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, vec(0.2, 0.2, 0.2, 1.0))
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)
        gl.glDepthFunc(gl.GL_LESS)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Position viewer.
        gl.glMatrixMode(gl.GL_MODELVIEW)
        # Position viewer.
        gl.glTranslatef(0.0, 0.0, -2.0);


    def OnDraw(self):
        # Clear color and depth buffers.
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        # Use a fresh transformation matrix.
        gl.glPushMatrix()
        # Position object.
        ## glTranslatef(0.0, 0.0, -2.0)
        gl.glRotatef(30.0, 1.0, 0.0, 0.0)
        gl.glRotatef(30.0, 0.0, 1.0, 0.0)

        gl.glTranslatef(0, -1, 0)
        gl.glRotatef(250, 1, 0, 0)

        gl.glEnable(gl.GL_BLEND)
        gl.glEnable(gl.GL_POLYGON_SMOOTH)
        gl.glMaterialfv(gl.GL_FRONT, gl.GL_AMBIENT_AND_DIFFUSE, vec(0.5, 0.5, 1.0, 0.5))
        gl.glMaterialf(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 1.0)
        gl.glShadeModel(gl.GL_FLAT)
        gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
        # glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

        base = .5
        height = 1.0
        slices = 16

        # Draw cone open ended without glu.
        tau = pi * 2
        gl.glBegin(gl.GL_TRIANGLE_FAN)
        centerX, centerY, centerZ = 0.0, 0.0, height
        gl.glVertex3f(centerX, centerY, centerZ)  # Center of circle.
        centerX, centerY, centerZ = 0.0, 0.0, 0.0
        for i in range(slices + 1):
            theta = tau * float(i) / float(slices)  # Get the current angle.
            x = base * cos(theta)  # Calculate the x component.
            y = base * sin(theta)  # Calculate the y component.
            gl.glVertex3f(x + centerX, y + centerY, centerZ)  # Output vertex.
        gl.glEnd()

        gl.glPopMatrix()
        gl.glRotatef((self.y - self.lasty), 0.0, 0.0, 1.0);
        gl.glRotatef((self.x - self.lastx), 1.0, 0.0, 0.0);
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

