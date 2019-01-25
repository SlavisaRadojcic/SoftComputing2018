# -*- coding: utf-8 -*-
"""
Created on Fri Jan  18 9:32:14 2019

@author: Slavisa Radojcic
"""
import numpy as np
import cv2
import pomocna1 as q
import pomocna2 as a
from keras import models
from racun import Racun
from scipy.spatial import distance
#import math
#expand = 4 # -> cnn == 88.25
expand = 6 # -> mlp = 88.81

'''
    Izbacivanje kontura koje se nalaze unutar drugih kontura
'''

def dmd(z):
    odbacene = []
    rez = []
    for i in range(len(z)):
        for j in range(len(z)):
            if i != j:
                t1,b1,c1,g1 = cv2.boundingRect(z[i])
                t2,b2,c2,g2 = cv2.boundingRect(z[j])
                
                t11 = t1 + c1
                b11 = b1 + g1
                t22 = t2 + c2
                b22 = b2 + c2
                if ((t1 <= t22) and (t22 <= t11)):
                    if ((b1 <= b22) and (b22 <= b11)):
                        odbacene.append(j)
    
    for i in range(len(z)):
        if not (i in odbacene):
            rez.append(z[i])
    return rez

def os(s):
    horizontalno, uspravno = s.shape
    okvir = np.zeros((horizontalno+2*expand, uspravno+2*expand))

    for m in range(expand,horizontalno+expand):
        for n in range(expand,uspravno+expand):
            okvir[m,n] = s[m-expand,n-expand]
    
    return okvir
    

def aproksimacija(m, odd):
    horizontalno, uspravno = odd.shape
    odd = os(odd)

    t = cv2.resize(odd, (28, 28), interpolation = cv2.INTER_CUBIC) #INTER_NEAREST)
    odradjena = t / 255

    # za mlp?
    odrav = odradjena.flatten()
    num = np.reshape(odrav, (1, 784))
    
    
    

    aprox = m.predict(num)
    end = np.argmax(aprox)
    print('Pretpostavljeni broj: ', end)
    return end
'''
    Nadji konture,obradi ih i izdvoji cifre
'''


def dodaj(slik):
    _, k, _ = cv2.findContours(slik, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
    dm = []
    for d in k:
        t,b,c,g = cv2.boundingRect(d)
        if c >= 5 and  c <= 25 and g >= 9 and g <= 25: #w>=5
            dm.append(d)
                
    dm = dmd(dm)
                
    for b in dm:
        t,b,c,g = cv2.boundingRect(b)
    fr = []
    
    for f in dm:
        t,b,c,g = cv2.boundingRect(f)

        u = Racun(t,b,c,g)
        fr.append(u)
            
    return fr

'''
     Prosledi broj kojem potom trazimo odgovarajuci u nizu
'''


def pron(i, bb):
    k = []

    for b in bb:
        long = distance.euclidean((i.t + i.c, i.b + i.g), (b.t + b.c,b.b +b.g))

        if long < 30:
            k.append([long, b])

    k = sorted(k, key=lambda x: x[0])   

    if len(k) > 0:
        return k[0][1]
    else:
        return None

'''
    Ažurira postojeće brojeve. Za svaki broj cemo pokrenuti funkciju 
	koja ce imati za cilj da pokusa da pronadje odgovarajuci broj iz drugog frejma, 
	Ako nađe, tom se broju azurira pozicija. Ako ga ne pronadje, onda se dodaje kao
    novi broj u listu. 
'''


def az(dd, mm):
    for d in dd:
        j = pron(d, mm)

        if j is None:
            mm.append(d)       
        else:
            j.bnl(d.t, d.b, d.c, d.g)

'''
    Metoda koja izbacuje predaleke brojeve(koji nisu od interesa)
'''

#removeFarAwayNumbers(numbers):
def ods(m):
    p = []
    for j in m:
        if (j.t + j.c < 620) and (j.b + j.g < 470):
        #if not (num.get_bottom_right()[1] > 470 or num.get_bottom_right()[0] > 620):
            p.append(j)
    
    return p

'''
    Crtanje brojeva na frejm
'''
def graf(dd, b):
    for d in dd:
        m = (int((d.x + (d.x + d.w)) / 2), int((d.y + (d.y + d.h)) / 2))
        cv2.putText(b, ('Width: ' + str(d.w) + ' Height: ' + str(d.h)), m, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 255), 1, cv2.LINE_AA)
        cv2.rectangle(b, (d.x,d.y), (d.x+d.w,d.y+d.h),(0,255,255),1)


'''
    Provera da li je broj prosao ispod linije
'''


def rampa(blt, O, k, dd):
    i = (int(dd.t), int(dd.b), 0)
    j, don, = q.stamp(i, k[0], k[1])
                    
    don = (int(don[0]), int(don[1]))
    brin = (int((dd.t + (dd.t + dd.c)) / 2), int((dd.b + (dd.b + dd.g)) / 2))
    
    if j > 20 and j < 15:
       return False
    elif j < 20 and j > 15:
        k1, l1 = a.mln(brin, O)
        jj = brin[1]/(brin[0]-O[0])
        
        '''
            Ugao između dve prave
            tgfi = (tgfi2 - tgfi1) / (1 + tgfi1*tgfi2)
            
            Ako je jj < blt, onda se broj nalazi ispod linije,
            što znači da je prošao ispod linije.
        '''
        if jj < blt:
            return True
        else:
     
            return False
        
    else:
        return False

'''
    Obrada video sadrzaja i upis u out.txt datoteku
'''
def sumiraj(video, file, m):
    cap = cv2.VideoCapture('../data/' + video)
    
    cv2.startWindowThread()
    
    flag, frame = cap.read()
    
    s = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, slik = cv2.threshold(s, 25, 255, cv2.THRESH_BINARY)
    
    #img_bin
    drag = a.fn(slik, frame)
    
    nn,ff = a.mln((drag[0][0], drag[0][1]), (drag[1][0], drag[1][1]))
    
    '''
        tačka u kojoj prava seče x osu
        u zavisnosti od nje će se računati tangens fi ugla 
        y = kx + l za y = 0
    '''
    O = (-ff/nn, 0)
    
    '''
    blt(tangensfi) = y / x
    '''
    blt = drag[0][1] / (drag[0][0] - O[0])
    
    rr = 0
    
    zz = []
    
    while(cap.isOpened()):
        flag, frame = cap.read()
        if flag:
            s = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, gg = cv2.threshold(s, 25, 255, cv2.THRESH_BINARY)
            
            
            cv2.line(frame, (drag[0][0],drag[0][1]), (drag[1][0], drag[1][1]), (0,255,0), 2)
            
            dd = dodaj(gg)
            
            if len(dd) > 0:
                az(dd, zz)
            
            '''
                Da li je broj prosao ispod linije? DA --> dodaje se na sumu.
            '''
            for uu in zz:
                if uu.ok == False:
                    if rampa(blt, O, drag, uu) == True:
                        uu.gj(True)
                        odr = gg[uu.b - expand:uu.b + uu.g + expand, uu.t - expand:uu.t + uu.c + expand]
                        vv = aproksimacija(m, odr)
                        rr += vv
                
            zz = ods(zz)
            
           
            
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
            
        # Izlazimo iz petlje na kraju videa
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            break
        
        
    cap.release()
    
    print('suma -> ', rr)
    file.write('\n' + video + '\t' + str(rr))



def main():
    if __name__ == '__main__':
        
        ml = models.load_model('model_mlp.h5') #model_cnn.h5
        
        #Otvaranje i zapisivanje u out.txt datoteku    
        out = open('out.txt', 'a')
        out.write('RA 191/2013 Slavisa Radojcic')
        out.write('\nfile\tsum')
        
        videos = ['video-0.avi', 'video-1.avi', 'video-2.avi', 'video-3.avi', 'video-4.avi', 'video-5.avi', 'video-6.avi', 'video-7.avi', 'video-8.avi', 'video-9.avi']
        print('Obrada video sadrzaja u toku')
        for video in videos:
            print(video)
            sumiraj(video, out, ml)
        print('Kraj obrade')
        
       


main()