import math
from conversion import bearing_to_radians


def gauss_kruger(latitude, longitude, central_meridian, proj):
    """ Convert lat,long to projected coordinates
    """
    # Change lat/long to decimal degrees and convert to radians
    rlat = bearing_to_radians(latitude)
    rlong = bearing_to_radians(longitude)
    rcentral_meridian = bearing_to_radians(central_meridian)

    a = proj.a
    invf = proj.invf
    m0 = proj.m0
    false_easting = proj.false_easting
    false_northing = proj.false_northing

    # Calculate geometrical constants
    f = 1.0/invf
    b = a * (1-f)  # semi - minor axis

    # Eccentricity
    e2 = 2 * f - f * f  # = f*(2-f) = (a^2-b^2)/a^2
    e = math.sqrt(e2)

    # Compute 3rd flattening and powers
    n = (a - b)/(a + b)
    n2 = n * n
    n3 = n * n2
    n4 = n2 * n2
    n5 = n3 * n2
    n6 = n2 * n4
    n7 = n4 * n3
    n8 = n4 * n4

    # Rectifying Radius A
    A = (a/(1+n)) * (1+(1.0/4.0) * n2 + (1.0/64) * n4 + (1.0/256) * n6 + (25.0/16384) * n8)

    # Calculate conformal latitude
    sigma = math.sinh( e*math.atanh(( e * math.tan(rlat)) / (math.sqrt( 1 + math.tan(rlat) * math.tan(rlat)))))
    conformal_lat = math.tan(rlat) * math.sqrt(1 + sigma * sigma) - sigma * \
                                                                   math.sqrt(1 + math.tan(rlat) * math.tan(rlat))

    # Compute the coefficients
    a2 = (1.0/2) * n - (2.0/3) * n2 + (5.0/16) * n3 + (41.0/180) * n4 - (127.0/288) * n5 + (7891.0/37800) * n6 +\
         (72161.0/387072) * n7 - (18975107.0/50803200) * n8
    a4 = (13.0/48) * n2 - (3.0/5) * n3 + (557.0/1440) * n4 + (281.0/630) * n5 - (1983433.0/1935360) * n6 + \
         (13769.0/28800) * n7 + (148003883.0/174182400) * n8
    a6 = (61.0/240) * n3 - (103.0/140) * n4 + (15061.0/26880) * n5 + (167603.0/181440) * n6 - \
         (67102379.0/29030400) * n7 + (79682431.0/79833600) * n8
    a8 = (49561.0/161280) * n4 - (179.0/168) * n5 + (6601661.0/7257600) * n6 + (97445.0/49896) * \
                                                                               n7 - (40176129013.0/7664025600) * n8
    a10 = (34729.0/80640)* n5-(3418889.0/1995840)* n6+(14644087.0/9123840)* n7+(2605413599.0/622702080) * n8
    a12 = (212378941.0/319334400) * n6 - (30705481.0/10378368) * n7 + (175214326799.0/58118860800) * n8
    a14 = (1522256789.0/1383782400) * n7 - (16759934899.0/3113510400) * n8
    a16 = (1424729850961.0/743921418240) * n8

    # Find w by subtracting central meridian from longitude
    w = rlong - rcentral_meridian # Converted to radians

    # Compute the gauss-Schreiber coordinates
    u = a * math.atan( conformal_lat/math.cos(w))
    v = a * math.asinh(math.sin(w) / (math.sqrt( conformal_lat * conformal_lat + math.cos(w) * math.cos( w))))

    # Calculate partial solutions for x and y to make calcs easier
    x1 = math.cos(2 * (u / a)) * math.sinh(2 * (v / a))
    x2 = math.cos(4 * (u / a)) * math.sinh(4 * (v / a))
    x3 = math.cos(6 * (u / a)) * math.sinh(6 * (v / a))
    x4 = math.cos(8 * (u / a)) * math.sinh(8 * (v / a))
    x5 = math.cos(10 * (u / a)) * math.sinh(10 * (v / a))
    x6 = math.cos(12 * (u / a)) * math.sinh(12 * (v / a))
    x7 = math.cos(14 * (u / a)) * math.sinh(14 * (v / a))
    x8 = math.cos(16 * (u / a)) * math.sinh(16 * (v / a))

    y1 = math.sin(2 * (u / a)) * math.cosh(2 * (v / a))
    y2 = math.sin(4 * (u / a)) * math.cosh(4 * (v / a))
    y3 = math.sin(6 * (u / a)) * math.cosh(6 * (v / a))
    y4 = math.sin(8 * (u / a)) * math.cosh(8 * (v / a))
    y5 = math.sin(10 * (u / a)) * math.cosh(10 * (v / a))
    y6 = math.sin(12 * (u / a)) * math.cosh(12 * (v / a))
    y7 = math.sin(14 * (u / a)) * math.cosh(14 * (v / a))
    y8 = math.sin(16 * (u / a)) * math.cosh(16 * (v / a))

    # Calculate partial solutions for q and p to make calcs easier
    q1 = math.sin(2 * (u / a)) * math.sinh(2 * (v / a))
    q2 = math.sin(4 * (u / a)) * math.sinh(4 * (v / a))
    q3 = math.sin(6 * (u / a)) * math.sinh(6 * (v / a))
    q4 = math.sin(8 * (u / a)) * math.sinh(8 * (v / a))
    q5 = math.sin(10 * (u / a)) * math.sinh(10 * (v / a))
    q6 = math.sin(12 * (u / a)) * math.sinh(12 * (v / a))
    q7 = math.sin(14 * (u / a)) * math.sinh(14 * (v / a))
    q8 = math.sin(16 * (u / a)) * math.sinh(16 * (v / a))

    p1 = math.cos(2 * (u / a)) * math.cosh(2 * (v / a))
    p2 = math.cos(4 * (u / a)) * math.cosh(4 * (v / a))
    p3 = math.cos(6 * (u / a)) * math.cosh(6 * (v / a))
    p4 = math.cos(8 * (u / a)) * math.cosh(8 * (v / a))
    p5 = math.cos(10 * (u / a)) * math.cosh(10 * (v / a))
    p6 = math.cos(12 * (u / a)) * math.cosh(12 * (v / a))
    p7 = math.cos(14 * (u / a)) * math.cosh(14 * (v / a))
    p8 = math.cos(16 * (u / a)) * math.cosh(16 * (v / a))

    # Calculate q and p for calculating point scale factor
    q = - (2 * a2 * q1 + 4 * a4 * q2 + 6* a6* q3 + 8 * a8 * q4 +
           10 * a10 * q5 + 12 * a12 * q6 + 14 * a14 * q7 + 16 * a16 * q8)
    p = 1 + (2 * a2 * p1 + 4 * a4 * p2 + 6 * a6 * p3 + 8 * a8 *
             p4 + 10 * a10 * p5 + 12 * a12 * p6 + 14 * a14 * p7 + 16 * a16 * p8)

    # Calculate point scale factor m
    m = m0 * (A / a)*math.sqrt(q * q + p * p) * (math.sqrt(1+(math.tan(rlat)*math.tan(rlat))) *
        math.sqrt(1 - e2*(math.sin(rlat)*math.sin(rlat))))/\
        math.sqrt(conformal_lat * conformal_lat+math.cos(w)*math.cos(w))

    grid_conv = math.atan(q / p)+math.atan((conformal_lat*math.tan(w))/math.sqrt(1 + conformal_lat * conformal_lat))*\
                180/math.pi

    # Calculate coordinates
    X = A*((v / a) + a2 * x1 + a4 * x2 + a6 * x3 + a8 * x4 + a10 * x5 + a12 * x6 + a14 * x7 + a16 * x8)
    Y = A*((u / a) + a2 * y1 + a4 * y2 + a6 * y3 + a8 * y4 + a10 * y5 + a12 * y6 + a14 * y7 + a16 * y8)

    # Calculate scaled coordinates with false easting and northing
    easting = false_easting + m0 * X
    northing = false_northing + m0 * Y

    return easting, northing, m, grid_conv
