class Racun:
    
    def __init__(self, t, b, c, g):
        self.t = t
        self.b = b
        self.c = c
        self.g = g
        self.ok = False
       
    def gh(self):
        return self.ok
    
    def gj(self, passed):
        self.ok = passed
        
    def __str__(self):
        return "X: {0}, Y: {1}, W: {2}, H: {3}".format(self.x, self.y, self.w, self.h)
    
    def bnl(self, t, b, c, g):
      self.t = t
      self.b = b
      self.c = c
      self.g = g
