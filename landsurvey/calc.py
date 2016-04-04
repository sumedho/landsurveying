import math

def join2d(pnt1, pnt2):
    """ Calculate bearing and distance from one point to the next
    """
    delta_n = pnt2.y - pnt1.y
    delta_e = pnt2.x - pnt1.x

    distance = math.sqrt(math.pow(delta_n, 2) + math.pow(delta_e, 2))

    bearing = math.degrees(math.atan2(delta_e, delta_n)) % 360

    if bearing < 0:
        bearing += 360

    return(distance, bearing)

def rad2d(pnt, bearing, distance):
    """ Calculate x,y given inital starting point, bearing and distance
    """
    x = pnt.x + distance * math.sin(math.radians(dms2dec(bearing)))
    y = pnt.y + distance * math.cos(math.radians(dms2dec(bearing)))

    return(x, y)