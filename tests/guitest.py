#!/usr/bin/python
from Tkinter import Tk, Canvas

class gui:
    
    def __init__(self):
        self.tk = Tk()
        self.canvas = Canvas(self.tk)
        self.tk.after_idle(self.test)
        self.tk.mainloop()

    def test(self):
        print 'boom'
        self.tk.after(200, self.test2)

    def test2(self):
        print 'bang'
        self.tk.after(200, self.test)

if __name__ == '__main__':
    b = gui()
