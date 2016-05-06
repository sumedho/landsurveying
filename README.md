
# Python Land Surveying Library
A python library which provides various land surveying calculations. It provides the following:
* conversion of decimal degrees to various formats
* classes for 2d point, 3d point and projection definition
* functions to compute joins, radiations and reduced levels
* various intersection routinues
* freestation resection using least squares
* gauss kruger to convert from latitude/longitude to projected grid system

___

### Import the library


```python
import landsurvey as ls
```

### Create points
Many of the functions in the library take points as input. These are created using the various classes available. 
* Points can be either 2d or 3d(i.e. have a z-value) 
* A code or id can be associated with every point but is optional


```python
point1 = ls.Point2d(10, 10)
point2 = ls.Point3d(20, 20, 20, "TOE")

print(point1.x, point1.y)
print(point2.x, point2.y, point2.z, point2.code)

```

    (10, 10)
    (20, 20, 20, 'TOE')
    

### Degrees conversion
Degrees can be converted from decimal degrees to degrees, minutes, seconds and vice versa. These routines use the HP format for degrees, minutes, seconds (i.e. dd.mmss).

For example:

20&deg;35'45" would be represented as 20.3545

144&deg;25'29.52442" would be represented as 144.252952442

Using the first example, it can be converted as follows


```python
a = ls.dms2dec(20.3545)
b = ls.dec2dms(a)
print "decimal degrees =", a
print "degrees, minutes, seconds =",b
```

    decimal degrees = 20.5958333333
    degrees, minutes, seconds = 20.3545
    

The second example is the same


```python
a = ls.dms2dec(144.252952442)
b = ls.dec2dms(a)
print "decimal degrees =", a
print "degrees, minutes, seconds =",b
```

    decimal degrees = 144.424867894
    degrees, minutes, seconds = 144.252952442
    
