import math
from conversion import dms2dec, dec2dms


def join2d(pnt1, pnt2):
    """ Calculate bearing and distance from one point to the next
    """
    delta_n = pnt2.y - pnt1.y
    delta_e = pnt2.x - pnt1.x

    distance = math.sqrt(math.pow(delta_n, 2) + math.pow(delta_e, 2))

    bearing = math.degrees(math.atan2(delta_e, delta_n)) % 360

    if bearing < 0:
        bearing += 360

    return distance, dec2dms(bearing)


def rad2d(pnt, bearing, distance):
    """ Calculate x,y given inital starting point, bearing and distance
    """
    x = pnt.x + distance * math.sin(math.radians(dms2dec(bearing)))
    y = pnt.y + distance * math.cos(math.radians(dms2dec(bearing)))

    return x, y


def rad3d(pnt, bearing, slope_distance, zenith_angle, height_instrument, height_target):
    """
        Calculate x,y,z given inital starting point and 3d vector
        pnt: 3d point with x, y and z
        bearing: the bearing in dd.mmss
        slope_distance: measured slope distance
        zenith angle: zenith angle
        height_instrument: height of instrument
        height_target: height of target
    """
    horizontal_distance = slope_distance * math.sin(math.radians(dms2dec(zenith_angle)))
    x = pnt.x + horizontal_distance * math.sin(math.radians(dms2dec(bearing)))
    y = pnt.y + horizontal_distance * math.cos(math.radians(dms2dec(bearing)))
    z = pnt.z + height_instrument + (slope_distance * math.cos(math.radians(dms2dec(zenith_angle)))) - height_target
    return x, y, z


def bearing_bearing_intersection(pnt_a, pnt_b, bearing_a, bearing_b):
    """
        Calculate position C given:
        point A and bearing to C from A
        point B and bearing to C from B
    """
    bc = math.tan(math.radians(dms2dec(bearing_b)))
    ac = math.tan(math.radians(dms2dec(bearing_a)))
    y = pnt_a.y + ((pnt_b.y - pnt_a.y) * bc - (pnt_b.x - pnt_a.x))/(bc - ac)
    x = pnt_a.x + (y - pnt_a.y) * ac

    return x, y

