def dms2dec(dms):
    """ Convert dd.mmss to decimal degrees
    """
    degrees = 0
    minutes = 0
    seconds = 0
    decdeg = 0
    sign = 0
    if dms < 0:
        sign = -1
        dms = dms * sign
    else:
        sign =1

    degrees = int(dms)
    minutes = int((dms*100)-degrees*100)
    seconds = (((dms-degrees)*100) - minutes) * 100
    decdeg = degrees + float(minutes)/60 + float(seconds)/3600
    return(decdeg*sign)

def dec2dms(decdeg):
    """ Convert decimal degrees to dd.mmss
    """
    degrees = 0
    minutes = 0
    seconds = 0
    dms = 0
    sign = 0
    if dms < 0:
        sign = -1
        dms = dms * sign
    else:
        sign =1

    degrees = int(decdeg)
    minutes = int((decdeg*60) - degrees*60)
    seconds = (((decdeg - degrees) * 3600) - minutes * 60)
    dms = degrees + float(minutes)/100 + seconds/10000
    return(dms)