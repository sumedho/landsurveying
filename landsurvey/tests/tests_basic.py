# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:32:32 2016

@author: derek.carter
"""

import unittest
import landsurvey as ls


class TestDmsConversions(unittest.TestCase):
    """
     Conversion of dd.mmss to decimal degrees tests
    """
    def test1(self):
        self.assertAlmostEquals(ls.dms2dec(20.3040), 20.511111111, places=9)
        
    def test2(self):
        self.assertAlmostEquals(ls.dms2dec(342.2630), 342.441666667, places=9)
        
    def test3(self):
        self.assertAlmostEquals(ls.dms2dec(180.0101), 180.016944444, places=9)
    
    def test4(self):
        self.assertAlmostEquals(ls.dms2dec(-359.5959), -359.999722222, places=9)

    def test5(self):
        self.assertAlmostEquals(ls.dms2dec(-2.1524), -2.256666667, places=9)


class TestDecimalConversions(unittest.TestCase):
    """
     Conversion of decimal degrees to dd.mmss tests
    """
    def test1(self):
        self.assertAlmostEquals(ls.dec2dms(20.511111111), 20.3040, places=4)
    
    def test2(self):
        self.assertAlmostEquals(ls.dec2dms(342.441666667), 342.2630, places=4)
        
    def test3(self):
        self.assertAlmostEquals(ls.dec2dms(180.016944444), 180.0101, places=4)
    
    def test4(self):
        self.assertAlmostEquals(ls.dec2dms(-359.999722222), -359.5959, places=4)

    def test5(self):
        self.assertAlmostEquals(ls.dec2dms(-2.256666667), -2.1524, places=9)
        

class TestJoin2d(unittest.TestCase):
    """
     2D join tests
    """
    def test1(self):
        point1 = ls.Point2d(32255.751, 49076.286)
        point2 = ls.Point2d(12231.864, 36939.667)
        (dist, bearing) = ls.join2d(point1, point2)
        
        expected_distance = 23414.815
        expected_bearing = 238.4647  # In dd.mmss

        self.assertAlmostEquals(dist, expected_distance, places=3)
        self.assertAlmostEquals(bearing, expected_bearing, places=3)


class TestRad3d(unittest.TestCase):
    """
        3D rad tests
    """
    def test1(self):
        point = ls.Point3d(255.751, 176.286, 42.623)
        height_instrument = 1.565
        height_target = 1.690
        bearing = 240.2520
        slope_distance = 11.682
        zenith_angle = 93.2230
        (x, y, z) = ls.rad3d(point, bearing, slope_distance, zenith_angle, height_instrument, height_target)

        expected_x = 245.609
        expected_y = 170.530
        expected_z = 41.810

        self.assertAlmostEquals(x, expected_x, places=3)
        self.assertAlmostEquals(y, expected_y, places=3)
        self.assertAlmostEquals(z, expected_z, places=3)

    def test2(self):
        point = ls.Point3d(301.245, 299.215, 35.214)
        height_instrument = 1.565
        height_target = 1.690
        bearing = 160.2520
        slope_distance = 15.162
        zenith_angle = 101.4430
        (x, y, z) = ls.rad3d(point, bearing, slope_distance, zenith_angle, height_instrument, height_target)

        expected_x = 306.219
        expected_y = 285.228
        expected_z = 32.004

        self.assertAlmostEquals(x, expected_x, places=3)
        self.assertAlmostEquals(y, expected_y, places=3)
        self.assertAlmostEquals(z, expected_z, places=3)


class TestRad2d(unittest.TestCase):
    """
        2D rad tests
    """
    def test1(self):
        point = ls.Point2d(177413.0, 446111.0)
        bearing = 12.3015  # dd.mmss
        distance = 6235.42
        (x, y) = ls.rad2d(point, bearing, distance)

        expected_x = 178763.03
        expected_y = 452198.52

        self.assertAlmostEquals(x, expected_x, places=2)
        self.assertAlmostEquals(y, expected_y, places=2)


class TestBearingBearingIntersection(unittest.TestCase):
    """
        bearing bearing intersection tests
    """
    def test1(self):
        pnt_a = ls.Point2d(422145.515, 1817938.975)
        pnt_b = ls.Point2d(398112.145, 1828011.324)
        bearing_ac = 237.14216
        bearing_bc = 165.53428
        (x, y) = ls.bearing_bearing_intersection(pnt_a, pnt_b, bearing_ac, bearing_bc)

        expected_x = 403635.851
        expected_y = 1806028.287

        self.assertAlmostEquals(x, expected_x, places=3)
        self.assertAlmostEquals(y, expected_y, places=3)

    def test2(self):
        pnt_a = ls.Point2d(2589.40, 6717.85)
        pnt_b = ls.Point2d(9307.04, 3423.63)
        bearing_ac = 62.2658
        bearing_bc = 359.4925
        (x, y) = ls.bearing_bearing_intersection(pnt_a, pnt_b, bearing_ac, bearing_bc)

        expected_x = 9286.143
        expected_y = 10211.467

        self.assertAlmostEquals(x, expected_x, places=3)
        self.assertAlmostEquals(y, expected_y, places=3)


class TestDistanceDistanceIntersection(unittest.TestCase):
    """
        distance distance intersection tests
    """
    def test1(self):
        pnt_a = ls.Point2d(1859.75, 3722.63)
        pnt_b = ls.Point2d(1078.37, 2405.38)
        dist_ac = 1537.75
        dist_bc = 2487.56

        expected_x1 = 850.038
        expected_y1 = 4882.439
        expected_x2 = 3361.660
        expected_y2 = 3392.568

        (x1, y1, x2, y2) = ls.distance_distance_intersection(pnt_a, pnt_b, dist_ac, dist_bc)

        self.assertAlmostEquals(x1, expected_x1, places=3)
        self.assertAlmostEquals(y1, expected_y1, places=3)
        self.assertAlmostEquals(x2, expected_x2, places=3)
        self.assertAlmostEquals(y2, expected_y2, places=3)


class TestTwoLineIntersection(unittest.TestCase):
    """
        two line intersection tests
    """
    def test1(self):
        pnt_a = ls.Point2d(1101.61, 1113.14)
        pnt_b = ls.Point2d(1134.86, 1061.14)
        pnt_c = ls.Point2d(1334.91, 1098.36)
        pnt_d = ls.Point2d(1358.31, 1211.90)
        (x, y) = ls.two_line_intersection(pnt_a, pnt_b, pnt_c, pnt_d)
        print(x, y)

    def test2(self):
        pnt_a = ls.Point2d(74184.946, 5404.450)
        pnt_b = ls.Point2d(74204.945, 5404.450)
        pnt_c = ls.Point2d(74185.176, 5399.176)
        pnt_d = ls.Point2d(74205.176, 5399.176)
        (x, y) = ls.two_line_intersection(pnt_a, pnt_b, pnt_c, pnt_d)
        print(x, y)

class TestGaussKruger(unittest.TestCase):
    """
     Gauss Kruger Tests
    """
    def test1(self):
        """
            Test of converting lat, long to MGA using Coordinates of Flinders Peak
            Taken from Page 46 of GDA Technical Manual 2.3
        """
        # Map Grid Australia Projection
        a = 6378137.0
        invf = 298.257222101
        m0 = 0.9996
        false_easting = 500000
        false_northing = 10000000
        p = ls.Projection(a, invf, m0, false_easting, false_northing)
        
        # Flinders peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.570372030
        lon = 144.252952442
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 273741.297
        expected_n = 5796489.777
        expected_k = 1.00023056 # point scale factor

        self.assertAlmostEquals(e, expected_e, places=3)
        self.assertAlmostEquals(n, expected_n, places=3)
        self.assertAlmostEquals(k, expected_k, places=3)
        
    def test2(self):
        """
            Test of converting lat, long to MGA using Coordinates of Bunninyong Peak
            Taken from Page 46 of GDA Technical Manual 2.3
        """
        # Map Grid Australia Projection
        a = 6378137.0
        invf = 298.257222101
        m0 = 0.9996
        false_easting = 500000
        false_northing = 10000000
        p = ls.Projection(a, invf, m0, false_easting, false_northing)
        
        # Bunninyong peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.391015611
        lon = 143.553538393
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 228854.052
        expected_n = 5828259.038
        expected_k = 1.00050567 # point scale factor

        self.assertAlmostEquals(e, expected_e, places=3)
        self.assertAlmostEquals(n, expected_n, places=3)
        self.assertAlmostEquals(k, expected_k, places=3)
        
    def test3(self):
        """
            Test of converting lat, long to MGA using Coordinates of Smeaton Peak
            Taken from Page 46 of GDA Technical Manual 2.3
        """
        # Map Grid Australia Projection
        a = 6378137.0
        invf = 298.257222101
        m0 = 0.9996
        false_easting = 500000
        false_northing = 10000000
        p = ls.Projection(a, invf, m0, false_easting, false_northing)
        
        # Smeaton peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.174973137
        lon = 143.590316717
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 232681.853
        expected_n = 5867898.031
        expected_k = 1.00048035 # point scale factor

        self.assertAlmostEquals(e, expected_e, places=3)
        self.assertAlmostEquals(n, expected_n, places=3)
        self.assertAlmostEquals(k, expected_k, places=3)
        
    def test4(self):
        """
            Test of converting lat, long to MGA using Coordinates of Bellarine
            Taken from Page 46 of GDA Technical Manual 2.3
        """
        # Map Grid Australia Projection
        a = 6378137.0
        invf = 298.257222101
        m0 = 0.9996
        false_easting = 500000
        false_northing = 10000000
        p = ls.Projection(a, invf, m0, false_easting, false_northing)
        
        # Bellarine peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -38.090522718
        lon = 144.364367715
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 290769.028
        expected_n = 5774686.632
        expected_k = 1.00013919 # point scale factor

        self.assertAlmostEquals(e, expected_e, places=3)
        self.assertAlmostEquals(n, expected_n, places=3)
        self.assertAlmostEquals(k, expected_k, places=3)
        
    def test5(self):
        """
            Test of converting lat, long to MGA using Coordinates of Arthurs Seat
            Taken from Page 46 of GDA Technical Manual 2.3
        """
        # Map Grid Australia Projection 
        a = 6378137.0
        invf = 298.257222101
        m0 = 0.9996
        false_easting = 500000
        false_northing = 10000000
        p = ls.Projection(a, invf, m0, false_easting, false_northing)
        
        # Arthurs Seat coordinates in lat,long MGA94 zone 55 == 147
        lat = -38.211312687
        lon = 144.570255485
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 320936.377
        expected_n = 5752958.469
        expected_k = 0.99999489   # point scale factor

        self.assertAlmostEquals(e, expected_e, places=3)
        self.assertAlmostEquals(n, expected_n, places=3)
        self.assertAlmostEquals(k, expected_k, places=3)
        
    
if __name__ == '__main__':
    unittest.main()