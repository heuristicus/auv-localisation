#!/usr/bin/python
from sonar_sim import sonar as snr, map_rep
from Tkinter import Tk, Canvas

class gui:

    def __init__(self, sonar):
        self.tk = Tk()
        self.canvas = Canvas(self.tk, height=800, width=800)
        self.canvas.pack()
        self.sonar = sonar
        self.draw_map()
        self.draw_move_points()
        self.delete_old = True
        self.tk.after(20,self.redraw)
        self.tk.mainloop()
        
    def redraw(self):
        if self.delete_old:
            self.canvas.delete('scan')
            self.canvas.delete('intersect')
            
        self.draw_sonar_data()
        check = self.sonar.sim_step()
        if check is not -1:
            self.tk.after(2000, self.redraw)
        
    def draw_sonar_data(self):
        #print 'data'
        for line in self.sonar.scan_lines:
            draw_line(self.canvas, line, tag='scan')
        for point in self.sonar.intersection_points:
            draw_point(self.canvas, point, tag='intersect')

    def draw_map(self):
        #print 'map'
        for line in self.sonar.map.lines:
            draw_line(self.canvas, line, tag='map')

    def draw_move_points(self):
        for point in self.sonar.get_move_list():
            draw_point(self.canvas, point[0], tag='mvpt')

def draw_line(canvas, line, tag=''):
    c = line.coords
    canvas.create_line(c[0][0], c[0][1], c[1][0], c[1][1], tags=tag)

def draw_point(canvas, point, tag=''):
    pt = point
    if not point: return
    canvas.create_oval(pt.x - 1, pt.y - 1, pt.x + 1, pt.y + 1, tags=tag)

def draw_circle_from_centre(canvas, radius, centre):
    # probably the wrong way around, technically, but since it's a
    # circle it makes no difference really.
    tl = Point(centre.x - radius, centre.y + radius)
    br = Point(centre.x + radius, centre.y - radius)
    canvas.create_oval(tl.x, tl.y, br.x, br.y)
