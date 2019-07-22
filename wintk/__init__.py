import clr
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import System as _sys
import System.Drawing as _dra
import System.Windows.Forms as _for

class WintkError(Exception): pass
ClrVersion = _sys.Environment.Version

if __name__ != '__main__': from .constants import *
else: from constants import *
import types
winformwids = types.ModuleType('winformwids')

_defmaster = None
def _getdefmaster():
    global _defmaster
    if _defmaster is None: Tk()
    return _defmaster

class BaseWidget:
    transtable = {
        'height' : 'Height',
        'width' : 'Width',
        'text' : 'Text'
    }
    def _new(self, cnf={}, **kw):
        self.config(cnf, **kw)
    def __init__(self, controlclass, cmdevent=None, master=None, cnf={}, **kw):
        self.control = controlclass()
        if master is None: self.master = _getdefmaster()
        else: self.master = master
        if cmdevent is not None:
            def cmdmeth(self, i, cmdevent=cmdevent):
                def caller(sender, e, i=i): i()
                getattr(self.control, cmdevent).__iadd__(_sys.EventHandler(caller))
            self.cmdmeth = cmdmeth
        else: self.cmdmeth = None
        self._new(cnf, **kw)
    def place_configure(self, x=0, y=0):
        self.control.Location = _dra.Point(x, y)
        self.master.form.Controls.Add(self.control)
        self.control.Visible = True
    def pack_configure(self, side=TOP):
        if   side == TOP:
            x = self.master['width'] // 2 - self['width'] // 2
            y = 0
            self.control.Anchor = _for.AnchorStyles.Top
        elif side == LEFT:
            x = 0
            y = self.master['height'] // 2 - self['height'] // 2
            self.control.Anchor = _for.AnchorStyles.Left
        elif side == RIGHT:
            x = self.master['width'] - self['width']
            y = self.master['height'] // 2 - self['height'] // 2
            self.control.Anchor = _for.AnchorStyles.Right
        elif side == BOTTOM:
            x = self.master['width'] // 2 - self['width'] // 2
            y = self.master['height'] - self['height']
            self.control.Anchor = _for.AnchorStyles.Bottom
        else: raise WintkError('Not valid side: %r' % side)
        self.place_configure(x, y)
    place = place_configure
    pack = pack_configure
    def mainloop(self):
        self.master.mainloop()
    def cget(self, item):
        return getattr(self.control, self.transtable[item])
    __getitem__ = cget
    def __setitem__(self, item, value):
        if   item == 'text': value = value.replace('\n', '\r\n')
        elif item == 'command':
            if self.cmdmeth is None:
                raise WintkError('invalid attr: %s; valid options are: %s' % (item, ', '.join(self.transtable)))
            self.cmdmeth(self, value)
            return
        item = self.transtable[item]
        if callable(item): item = item(self.control, value)
        else: setattr(self.control, item, value)
    def configure(self, cnf={}, **kw):
        kw.update(cnf)
        for (key, item) in kw.items():
            self[key] = item
    config = configure
def _(self, size):
    self.Size = _dra.Size(*size)
BaseWidget.transtable['size'] = _

class Tk(BaseWidget):
    def __init__(self, cnf={}, **kw):
        global _defmaster
        _defmaster = self
        self.form = _for.Form()
        self.control = self.form
        self._new(cnf, **kw)
    def mainloop(self):
        _for.Application.EnableVisualStyles()
        _for.Application.Run(self.form)
    def destroy(self):
        self.form.Close()
    def geometry(self, info):
        info = info.split('+', 1)
        info[0] = info[0].split('x', 1)
        info[0][0], info[0][1] = int(info[0][0]), int(info[0][1])
        self['size'] = info[0]
    def title(self, text=None):
        if text is not None: self['text'] = text
        else: return self['text']
class Toplevel(Tk):
    def __init__(self, master=None, cnf={}, **kw):
        BaseWidget.__init__(self, _for.Form, None, master, cnf, **kw)
        self.form = self.control
        self.form.Show()

class Label(BaseWidget):
    def __init__(self, master=None, cnf={}, **kw):
        BaseWidget.__init__(self, _for.Label, None, master, cnf, **kw)

class Button(BaseWidget):
    def __init__(self, master=None, cnf={}, **kw):
        BaseWidget.__init__(self, _for.Button, 'Click', master, cnf, **kw)

class Entry(BaseWidget):
    def __init__(self, master=None, cnf={}, **kw):
        BaseWidget.__init__(self, _for.TextBox, None, master, cnf, **kw)

class Text(Entry):
    def __init__(self, master=None, cnf={}, **kw):
        Entry.__init__(self, master, cnf, **kw)
        self.control.Multiline = True
    def insert(self, where, what):
        what  = what.replace('\n', '\r\n')
        where = where.split('.')
        row = int(where[0]) - 1
        col = int(where[1])
        txtlist = (self['text']).splitlines()
        if row < len(txtlist):
            line = txtlist[row]
            line = line[:col] + what + line[col:]
            txtlist[row] = line
        else: txtlist.append(what)
        self['text'] = '\n'.join(txtlist)

# for clsname in dir(_for):
#     cls = getattr(_for, clsname)
#     if clsname[0] != '_' and isinstance(cls, type):
#         class _Sub(BaseWidget, cls): pass
#         setattr(winformwids, clsname, _Sub)
    
def mainloop():
    _getdefmaster().mainloop()

# Test:

def _test():
    root = Tk(size=(1000, 1000))
    text = "This is CLR version %s" % ClrVersion
    text += "\nThis should be a cedilla: \xe7"
    label = Label(root, text=text, size=(500, 500))
    label.pack()
    # label.pack()
    # test = Button(root, text="Click me!",
    #           command=lambda root=root: root.test.configure(
    #               text="[%s]" % root.test['text']))
    btn = Button(root, text='Push Me!', size=(500, 500), command=(lambda: print('SPAM!')))
    btn.pack(BOTTOM)
    # test.pack()
    # root.test = test
    # quit = Button(root, text="QUIT", command=root.destroy)
    # quit.pack()
    # The following three commands are needed so the window pops
    # up on top on Windows...
    # root.iconify()
    # root.update()
    # root.deiconify()
    root.mainloop()

if __name__ == '__main__':
    _test()