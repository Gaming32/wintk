import sys
TclVersion = None
TkVersion = None
ClrVersion = None

if sys.platform[:3] == 'win':
    from wintk import *
else: from tkinter import *

def _test():
    root = Tk()
    root.geometry('1000x1000')
    sub = Toplevel()
    sub.title('I am a sub...')
    Entry(sub, text='Name').pack()
    msg = Text(sub, width=200, height=200)
    sub['height'] = 500
    msg.pack(side=BOTTOM)
    msg.insert('1.0', 'Message')
    text  = "This is CLR version %s\n" % ClrVersion
    text += "This is TCL Version %s\n" % TclVersion
    text += "This is TK Version %s\n" % TkVersion
    text += "\nThis should be a cedilla: \xe7"
    label = Label(root, text=text, width=200, height=200)
    label.place(x=0, y=0)
    # label.pack()
    # test = Button(root, text="Click me!",
    #           command=lambda root=root: root.test.configure(
    #               text="[%s]" % root.test['text']))
    btn = Button(root, text='Push Me!', width=500, height=500, command=(lambda: print('SPAM!')))
    btn.place(x=0, y=100)
    # test.pack()
    # root.test = test
    quit = Button(root, text="QUIT", command=root.destroy)
    quit.pack()
    # The following three commands are needed so the window pops
    # up on top on Windows...
    # root.iconify()
    # root.update()
    # root.deiconify()
    root.mainloop()

if __name__ == '__main__':
    _test()