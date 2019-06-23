import clr
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')

import System as _sys
import System.Drawing as _dra
import System.Windows.Forms as _for

TkVersion = float(-1)
TclVersion = float(-1)

_defmaster = None
def _getdefmaster():
    global _defmaster
    if _defmaster is None: Tk()
    return _defmaster

class Tk:
    def __init__(self):
        global _defmaster
        _defmaster = self
        self.form = _for.Form()
    def mainloop(self):
        _for.Application.EnableVisualStyles()
        _for.Application.Run(self.form)
    def destroy(self):
        self.form.close()

class BaseWidget:
    transtable = {
        'height' : 'Height',
        'width' : 'Width',
        'text' : 'Text'
    }
    def __init__(self, controlclass, master, cnf={}, **kw):
        self.control = controlclass()
        self.master = master
        self.master.form.Controls.Add(self.control)
        self.config(cnf, **kw)
    def cget(self, item):
        return getattr(self.control, self.transtable[item])
    __getitem__ = cget
    def __setitem__(self, item, value):
        if item == 'text': value = value.replace('\n', '\r\n')
        setattr(self.control, self.transtable[item], value)
    def configure(self, cnf={}, **kw):
        kw.update(cnf)
        for (key, item) in kw.items():
            self[key] = item
    config = configure

class Label(BaseWidget):
    def __init__(self, master, cnf={}, **kw):
        BaseWidget.__init__(self, _for.Label, master, cnf, **kw)
    
def mainloop():
    _getdefmaster().mainloop()

# Test:

def _test():
    root = Tk()
    text = "This is Tcl/Tk version %s" % TclVersion
    text += "\nThis should be a cedilla: \xe7"
    label = Label(root, text=text, width=500, height=500)
    # label.pack()
    # test = Button(root, text="Click me!",
    #           command=lambda root=root: root.test.configure(
    #               text="[%s]" % root.test['text']))
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