import math
from conversion import dms2dec, dec2dms


def join2d(pnt1, pnt2):
    """ Calculate bearing and distance from point 1 to point 2

        Args:
            pnt1 (Point2d class): first point
            pnt2 (Point2d class): second point

        Returns:
            distance: the distance between points
            bearing: the bearing in degrees, minutes, seconds (dd.mmss)
    """
    delta_n = pnt2.y - pnt1.y
    delta_e = pnt2.x - pnt1.x

    distance = math.sqrt(math.pow(delta_n, 2) + math.pow(delta_e, 2))

    bearing = math.degrees(math.atan2(delta_e, delta_n)) % 360

    if bearing < 0:
        bearing += 360

    return distance, dec2dms(bearing)


def rad2d(pnt, bearing, distance):
    """ Calculate the new point x,y given initial starting point, bearing and distance

        Args:
            pnt (Point2d class):  The starting point
            bearing (floating point): The bearing in degrees, minutes, seconds (dd.mmss)
            distance (floating point): The distance

        Returns:
             x: x value of new point
             y: y value of new point
    """
    x = pnt.x + distance * math.sin(math.radians(dms2dec(bearing)))
    y = pnt.y + distance * math.cos(math.radians(dms2dec(bearing)))

    return x, y


def reduced_level(rla, hi, sd, za, ht):
    """ Calculates a reduced level

        Args:
            rla: reduced level of point a
            hi: height of instrument
            sd: slope distance
            za: zenith angle in dd.mmss (degrees, minutes, seconds)
            ht: height of target

        Returns:
            rlb: The reduced level at point b
    """
    za = math.radians(dms2dec(za))
    delta = -1 * (hi + sd*math.cos(za) - ht)
    rlb = rla + delta

    return rlb


def rad3d(pnt, bearing, slope_distance, zenith_angle, height_instrument, height_target):
    """ Calculate x,y,z given inital starting point and 3d vector

        Args:
            pnt (Point3d class): 3d point with x, y and z
            bearing: the bearing in degrees, minutes, seconds (dd.mmss)
            slope_distance: measured slope distance
            zenith_angle: zenith angle in degrees, minutes and seconds (dd.mmss)
            height_instrument: height of instrument
            height_target: height of target

        Returns:
            x: x value of new point
            y: y value of new point
            z: z value of new point
    """
    horizontal_distance = slope_distance * math.sin(math.radians(dms2dec(zenith_angle)))
    x = pnt.x + horizontal_distance * math.sin(math.radians(dms2dec(bearing)))
    y = pnt.y + horizontal_distance * math.cos(math.radians(dms2dec(bearing)))
    z = pnt.z + height_instrument + (slope_distance * math.cos(math.radians(dms2dec(zenith_angle)))) - height_target
    return x, y, z


def bearing_bearing_intersection(pnt_a, pnt_b, bearing_a, bearing_b):
    """ Calculate point c using a two bearings intersection:

        Args:
            pnt_a (Point2d class): point a
            pnt_b (Point2d class): point b
            bearing_a: bearing from a to c in degrees, minutes, seconds (dd.mmss)
            bearing_b: bearing from b to c in degrees, minutes, seconds (dd.mmss)

        Returns:
            x: x position of c
            y: y position of c
    """
    bc = math.tan(math.radians(dms2dec(bearing_b)))
    ac = math.tan(math.radians(dms2dec(bearing_a)))
    y = pnt_a.y + ((pnt_b.y - pnt_a.y) * bc - (pnt_b.x - pnt_a.x))/(bc - ac)
    x = pnt_a.x + (y - pnt_a.y) * ac

    return x, y


def distance_distance_intersection(pnt_a, pnt_b, dist_ac, dist_bc):
    """ Calculate point c using a two bearings intersection

        Returns the two calculated intersection points. It is
        up to the end user to decide which one they want.

        Args:
            pnt_a (Point2d class): point a
            pnt_b (Point2d class): point b
            dist_ac: distance from a to c
            dist_bc: distance from b to c

        Returns:
            x1: first x position of c
            y1: first y position of c
            x2: second x position of c
            y2: second y position of c
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
    """ Calculate the intersection of two lines given four points a, b, c, d

        If the lines do not intersect, then the string "NA" is returned for both x and y
        otherwise the intersection points x, y are returned

        Args:
            pnt_a (Point class): point a
            pnt_b (Point class): point b
            pnt_c (Point class): point c
            pnt_d (Point class): point d

        Returns:
            x: x-intersection or 'NA'
            y: y-intersection or 'NA'
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
