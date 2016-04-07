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


def distance_distance_intersection(pnt_a, pnt_b, dist_ac, dist_bc):
    """
        Calculate position C given:
        point A and distance to C from A
        point B and distance to C from B

        Uses Intersection of two circles algorithm
    """
    d2 = math.pow((pnt_b.x - pnt_a.x),2) + math.pow((pnt_b.y-pnt_a.y),2)
    d = math.sqrt(d2)
    s = (dist_ac + dist_bc + d)/2
    K = math.sqrt(s * (s-dist_bc) * (s - dist_ac) * (s - d))

    x1 = (pnt_b.x + pnt_a.x)/2 + (pnt_b.x - pnt_a.x) * (dist_ac*dist_ac - dist_bc*dist_bc)/(2*d2) \
        + 2 * (pnt_b.y - pnt_a.y)*K/d2
    y1 = (pnt_b.y + pnt_a.y) / 2 + (pnt_b.y - pnt_a.y) * (dist_ac * dist_ac - dist_bc * dist_bc) / (2 * d2) \
        - 2 * (pnt_b.x - pnt_a.x) * K / d2
    x2 = (pnt_b.x + pnt_a.x) / 2 + (pnt_b.x - pnt_a.x) * (dist_ac * dist_ac - dist_bc * dist_bc) / (2 * d2) \
        - 2 * (pnt_b.y - pnt_a.y) * K / d2
    y2 = (pnt_b.y + pnt_a.y) / 2 + (pnt_b.y - pnt_a.y) * (dist_ac * dist_ac - dist_bc * dist_bc) / (2 * d2) \
        + 2 * (pnt_b.x - pnt_a.x) * K / d2

    return x1, y1, x2, y2


def two_line_intersection(pnt_a, pnt_b, pnt_c, pnt_d):
    """
        Calculate the intersection of two lines given four points a, b, c, d

        If the lines do not intersect, then the string "NA" is returned for both x and y
        otherwise the intersection points x, y are returned
    """
    denominator = (pnt_a.x - pnt_b.x) * (pnt_c.y - pnt_d.y) - (pnt_a.y - pnt_b.y) * (pnt_c.x - pnt_d.x)

    # If denominator is zero, then the lines do not intersect
    if round(denominator, 3) == 0:
        x = "NA"
        y = "NA"
        return x, y
    else:
        K = ((pnt_b.x - pnt_a.x) * (pnt_d.y - pnt_b.y) - (pnt_b.y - pnt_a.y) * (pnt_d.x - pnt_b.x))/ \
            ((pnt_c.x - pnt_a.x) * (pnt_d.y - pnt_b.y) - (pnt_c.y - pnt_a.y) * (pnt_d.x - pnt_b.x))
        x = pnt_a.x + K * (pnt_c.x - pnt_a.x)
        y = pnt_a.y + K * (pnt_c.y - pnt_a.y)
        return x, y
