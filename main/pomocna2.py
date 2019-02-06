import cv2
import numpy as np

# Definisanje potrebnih konstanti i globalnih varijabli
minLL = 80
maxLG = 100

def mln(u1, u2):
    t1 = u1[0]
    b1 = u1[1]
    t2 = u2[0]
    b2 = u2[1]
    gg = np.float64((b2 - b1)) / (t2 - t1)
    ff = b1 - gg*t1
    return (gg,ff)

'''
    Linija preko Hougha
'''
def fn(slik, frame):
    nb = []
    tt = cv2.HoughLinesP(slik, 1, np.pi/180, 180, 200, 150)
    if tt is not None:
        for t1,b1,t2,b2 in tt[0]:
            cv2.line(frame, (t1,b1),(t2,b2), (0,255,0), 2)
            nb.append((t1,b1,0))
            nb.append((t2,b2,0))
    # Koordinate pocetne i krajnje tačke linije
    return nb
