# BEARING_CONVENTION is a constant which defines the type of bearing convention used.
# 1 = degrees, minutes, seconds (dd.mmss)
# 2 = North American quadrants (Ndd.mmssE)
# 3 = gradians

import math

BEARING_CONVENTION = 1

def convert_to_radians(bearing):
    """ Converts bearing to radians based on BEARING_CONVENTION
    """

    # degrees, minutes, seconds
    if BEARING_CONVENTION == 1:
        radians = math.radians(dms2dec(bearing))
        return(radians)

    # quadrants
    if BEARING_CONVENTION == 2:
        bearing = list(bearing)
        quad1 = bearing.pop(0) # Grab the first quadrant off front
        quad2 = bearing.pop(-1) # Grab second quadrant off back
        bearing = float(''.join(bearing)) # Convert remaining to a float number
        dec = dms2dec(bearing) # Convert to decimal degrees

        if quad1 == 'N' and quad2 == 'E':
            radians = math.radians(dec)

        if quad1 == 'S' and quad2 == 'E':
            radians = math.radians(180 - dec)

        if quad1 == 'S' and quad2 == 'W':
            radians = math.radians(180 + dec)

        if quad1 == 'N' and quad2 == 'W':
            radians = math.radians(360 - dec)

        return(radians)

    # gradians
    if BEARING_CONVENTION == 3:
        radians = bearing * (math.pi/200)
        return(radians)

def dms2dec(dms):
    """ Convert dd.mmss to decimal degrees
    """
    if dms < 0:
        sign = -1
        dms = dms * sign
    else:
        sign =1

    degrees = int(dms)
    minutes = int((dms*100)-degrees*100)
    seconds = (((dms-degrees)*100) - minutes) * 100
    decdeg = degrees + float(minutes)/60 + float(seconds)/3600
    return decdeg*sign


def dec2dms(decdeg):
    """ Convert decimal degrees to dd.mmss
    """
    if decdeg < 0:
        sign = -1
        decdeg = decdeg * sign
    else:
        sign = 1

    degrees = int(decdeg)
    minutes = int((decdeg*60) - degrees*60)
    seconds = (((decdeg - degrees) * 3600) - minutes * 60)
    dms = degrees + float(minutes)/100 + seconds/10000
    return dms*sign
