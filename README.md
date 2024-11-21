This is a small repository to help debug [printrun issue 1390][1]. It's based
on a striped down wxPython's [GLCanvas example][2]. And currently includes:

- pyopengl.py - an initial pyopengl version of the example
- pyglet-1.5-bad.py - a pyglet port of the example; has the same problem as
  pronterface: the Canvas doesn't diplay anything (a least on linux).
- pyglet-1.5-good.py - surprisingly works. The only difference is that
  pyglet.gl is imported as `from pyglet import gl` instead of 
  `from pyglet.gl import *`

[1]: https://github.com/kliment/Printrun/issues/1390
[2]: https://github.com/wxWidgets/Phoenix/blob/master/demo/GLCanvas.py
