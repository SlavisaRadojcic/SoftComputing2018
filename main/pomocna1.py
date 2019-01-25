import math

# Preuzeto sa http://www.fundza.com/vectors/point2line/index.html

def d(o,r):
	t,b,c = o
	T,B,C = r
	return t*T + b*B + c*C

def l(r):
	t,b,c = r
	return math.sqrt(t*t + b*b + c*c)
#vektor
def n(o,r):
	t,b,c = o
	T,B,C = r
	return (T-t, B-b, C-c)
#unit
def c(r):
	t,b,c = r
	d = l(r)
	return (t/d, b/d, c/d)
#distance
def o(r0,r1):
	return l(n(r0,r1))
#scale
def uv(o,r):
	t,b,c = o
	return (t * r, b * r, c * r)

def p(o,r):
	t,b,c = o
	T,B,C = r
	return (t+T, b+B, c+C)

# Given a line with coordinates 'start' and 'end' and the
# coordinates of a point 'pnt' the proc returns the shortest 
# distance from pnt to the line and the coordinates of the 
# nearest point on the line.
#
# 1  Convert the line segment to a vector ('line_vec').
# 2  Create a vector connecting start to pnt ('pnt_vec').
# 3  Find the length of the line vector ('line_len').
# 4  Convert line_vec to a unit vector ('line_unitvec').
# 5  Scale pnt_vec by line_len ('pnt_vec_scaled').
# 6  Get the dot product of line_unitvec and pnt_vec_scaled ('t').
# 7  Ensure t is in the range 0 to 1.
# 8  Use t to get the nearest location on the line to the end
#    of vector pnt_vec_scaled ('nearest').
# 9  Calculate the distance from nearest to pnt_vec_scaled.
# 10 Translate nearest back to the start/end line. 
# Malcolm Kesson 16 Dec 2012

def stamp(x, po, k):
	line_n = n(po, k)
	point_n = n(po, x)
	line_l= l(line_n)
	line_c = c(line_n)
	point_uv = uv(point_n, 1.0/line_l)
	g = d(line_c, point_uv)
	if g < 0.0:
		g = 0.0
	elif g > 1.0:
		g = 1.0
	s = uv(line_n, g)
	mov = o(s, point_n)
	dist = p(s, po)
	return (mov, dist)