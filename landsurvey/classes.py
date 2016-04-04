class Projection:
    def __init__(self, a, invf, m0, false_easting, false_northing):
        self.a = a # ellipsoid semi-major axis
        self.invf = invf # 1/f
        self.m0 = m0 # central scale factor
        self.false_easting = false_easting # false easting
        self.false_northing = false_northing # false northing

class Point2d:
    def __init__(self, x, y, code = None):
        if code is None:
            self.x = x
            self.y = y
        else:
            self.x = x
            self.y = y
            self.code = code

class Point3d:
    def __init__(self, x, y, z, code = None):
        if code is None:
            self.x = x
            self.y = y
            self.z = z
        else:
            self.x = x
            self.y = y
            self.z = z
            self.code = code