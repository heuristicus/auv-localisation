#!/usr/bin/python

from Tkinter import Tk, Canvas
import s_math

def main():
    rng = 5
    pt_dict = {'1': '84,68', '2': '84,136','3': '155,68','4': '155,136','5': '214,68','6': '214,136','7': '276,68','8': '276,136','9': '327,68','10': '327,136','11': '366,25','12': '366,136','13': '353,204','14': '353,272','15': '295,204','16': '295,272','17': '353,348','18': '353,408','19': '353,476','20': '295,348','21': '295,408','22': '295,476'}

    r = Tk()
    c = Canvas(r, width=400, height=600)
    c.pack()
    global pts, ovals, smath
    smath = s_math.SonarMath()
    pts = []
    ovals = []
    for key in pt_dict:
        a = map(int, pt_dict[key].split(','))
        pts.append(a)
        c.create_oval(a[0] -1, a[1] -1, a[0] + 1, a[1] + 1)
        c.create_oval(a[0] - 10, a[1] -10, a[0] + 10, a[1] + 10, state='hidden', tags='click')
    
    c.bind("<Button-1>", path)

    r.mainloop()

def path(event):
    x = event.x
    y = event.y
    global mv
    for pt in pts:
        if pt_dist(pt, [x,y]) <= 10:
            mv.append(pt)

    print mv

def pt_dist(p1, p2):
    return 

if __name__ == '__main__':
    main()
