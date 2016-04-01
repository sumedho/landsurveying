# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 14:32:32 2016

@author: derek.carter
"""

import unittest
import landsurveying as ls

"""
 Conversion of dd.mmss to decimal degrees tests
"""
class test_dms_conversions(unittest.TestCase):
    def test1(self):
        self.assertEqual(round(ls.dms2dec(20.3040),9), 20.511111111)
        
    def test2(self):
        self.assertEqual(round(ls.dms2dec(342.2630),9), 342.441666667)
        
    def test3(self):
        self.assertEqual(round(ls.dms2dec(180.0101),9), 180.016944444) 
    
    def test4(self):
        self.assertEqual(round(ls.dms2dec(-359.5959),9), -359.999722222)

"""
 Conversion of decimal degrees to dd.mmss tests
"""
class test_decimal_conversions(unittest.TestCase):
    def test1(self):
        self.assertEqual(round(ls.dec2dms(20.511111111),4), 20.3040)
    
    def test2(self):
        self.assertEqual(round(ls.dec2dms(342.441666667),4), 342.2630)
        
    def test3(self):
        self.assertEqual(round(ls.dec2dms(180.016944444),4), 180.0101)
    
    def test4(self):
        self.assertEqual(round(ls.dec2dms(-359.999722222),4), -359.5959)

"""
 Gauss Kruger Tests
"""
class test_gauss_kruger(unittest.TestCase):
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
        p = ls.projection(a, invf, m0, false_easting, false_northing)
        
        # Flinders peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.570372030
        lon = 144.252952442
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 273741.297
        expected_n = 5796489.777
        expected_k = 1.00023056 # point scale factor
        
        self.assertEqual(round(e,3), expected_e)
        self.assertEqual(round(n,3), expected_n)
        self.assertEqual(round(k,8), expected_k)
        
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
        p = ls.projection(a, invf, m0, false_easting, false_northing)
        
        # Bunninyong peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.391015611
        lon = 143.553538393
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 228854.052
        expected_n = 5828259.038
        expected_k = 1.00050567 # point scale factor
        
        self.assertEqual(round(e,3), expected_e)
        self.assertEqual(round(n,3), expected_n)
        self.assertEqual(round(k,8), expected_k)
        
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
        p = ls.projection(a, invf, m0, false_easting, false_northing)
        
        # Smeaton peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -37.174973137
        lon = 143.590316717
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 232681.853
        expected_n = 5867898.031
        expected_k = 1.00048035 # point scale factor
        
        self.assertEqual(round(e,3), expected_e)
        self.assertEqual(round(n,3), expected_n)
        self.assertEqual(round(k,8), expected_k)
        
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
        p = ls.projection(a, invf, m0, false_easting, false_northing)
        
        # Bellarine peak coordinates in lat,long MGA94 zone 55 == 147
        lat = -38.090522718
        lon = 144.364367715
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 290769.028
        expected_n = 5774686.632
        expected_k = 1.00013919 # point scale factor
        
        self.assertEqual(round(e,3), expected_e)
        self.assertEqual(round(n,3), expected_n)
        self.assertEqual(round(k,8), expected_k)
        
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
        p = ls.projection(a, invf, m0, false_easting, false_northing)
        
        # Arthurs Seat coordinates in lat,long MGA94 zone 55 == 147
        lat = -38.211312687
        lon = 144.570255485
        cm = 147
        (e, n , k, gc) = ls.gauss_kruger(lat, lon, cm, p)
        
        expected_e = 320936.377
        expected_n = 5752958.469
        expected_k = 0.99999489 # point scale factor
        
        self.assertEqual(round(e,3), expected_e)
        self.assertEqual(round(n,3), expected_n)
        self.assertEqual(round(k,8), expected_k)
        
    
if __name__ == '__main__':
    unittest.main()