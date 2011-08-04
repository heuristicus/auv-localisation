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

def draw_line(canvas, line, tag=''):
    c = line.coords
    canvas.create_line(c[0][0], c[0][1], c[1][0], c[1][1], tags=tag)

def draw_point(canvas, point, weight=0, colour='black', tag=''):
    pt = point
    if not point: return
    if weight == 0:
        canvas.create_oval(pt.x - 1, pt.y - 1, pt.x + 1, pt.y + 1, tags=tag, outline=colour)
    else:
        canvas.create_oval(pt.x - weight*5, pt.y - weight*5, pt.x + weight*5, pt.y + weight*5, tags=tag, outline=colour)

if __name__ == '__main__':
    b = gui()
