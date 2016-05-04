import math
from conversion import dms2dec, dec2dms
import numpy as np


def freestation_2point(data):
    """ Calculate a 2 point freestation(resection) using
        least squares given a bearing/distance to each point from unknown point U.

        Args:
            data (np.array): matrix containing two rows of [x, y, horizontal distance, bearing(dms)]

        Return:
            xu: x value of unknown point
            yu: y value of unknown point
            v: variance matrix
            cnt: number of iterations till convergence
    """
    dist_sd = 1/((0.001*0.001))  # distance standard deviation
    ang_sd = 1/(5*5)  # angle standard deviation

    # Station coords for 2 station resection
    xa = data[0, 0]
    ya = data[0, 1]
    xb = data[1, 0]
    yb = data[1, 1]

    az_a = data[0, 3]
    az_b = data[1, 3]

    # Measured distances from unknown station U to A,B
    dist_au = data[0, 2]
    dist_bu = data[1, 2]

    # Calculate an initial approximation for the unknown station U
    # this calculation is performed using modifications of a two-point resection algorithm
    # found in "A field-ready solution to the resection problem given two coordinated points"
    # by P Milburn and R Allaby Canadian Agricultural Engineering Vol 29, No 1 Winter 1987.
    x = xb - xa  # get difference in x direction between resection point b and a
    y = yb - ya  # get difference in y direction between resection point b and a

    dist_ab = math.sqrt((xb-xa)*(xb-xa)+(yb-ya)*(yb-ya))

    # Calculate the angle a1 and handle various cases
    if xb < xa:
        a1 = 0.5 * math.pi - math.atan2(y, x)
    if xb > xa:
        a1 = 0.75 * math.pi - math.atan2(y, x)
    if xb == xa and yb > ya:
        a1 = math.pi
    if xb == xa and yb < ya:
        a1 = 0

    # Calculate the interior angle from resection point A to point B
    ang_uab = math.radians(dms2dec(az_b)) - math.radians(dms2dec(az_a))
    b = math.asin(dist_au * math.sin(ang_uab)/dist_ab)
    a = math.asin(dist_bu * math.sin(ang_uab)/dist_ab)

    a2 = a1 - b  # Calculate angle a2
    a3 = 2 * math.pi + (a1 - math.pi + a)  # Calculate angle a3

    # Calculate initial (x,y) coordinates for unknown station U from remote point B
    bx = xb + math.sin(a2) * dist_bu
    by = yb + math.cos(a2) * dist_bu

    # Calculate initial (x,y) coordinates for unknown station U from remote point A
    ax = xa + math.sin(a3) * dist_au
    ay = ya + math.cos(a3) * dist_au

    xu = (bx + ax)/2  # the averaged initial x coordinate of the unknown station U
    yu = (by + ay)/2  # the averaged initial y coordinate of the unknown station U

    # The least squares adjustment starts here. The intial coodinates xu and yu
    # for the unknown station are used as the start of the least squares adjustment

    w = np.diag([dist_sd, dist_sd, ang_sd, ang_sd])

    cnt = 1
    # maximum iterations is 20, this avoids an infinite loop if there is no solution
    for i in range(1, 20):
        au = math.sqrt((xu - xa)*(xu - xa) + (yu - ya)*(yu - ya))
        bu = math.sqrt((xu - xb)*(xu - xb) + (yu - yb)*(yu - yb))

        # Jacobian matrix elements for distances
        j11 = (xu - xa) / au
        j12 = (yu - ya) / au
        j21 = (xu - xb) / bu
        j22 = (yu - yb) / bu

        # Jacobian matrix elements for angles
        j31 = (ya - yu) / (au *au)
        j32 = (xa - xu) / (au *au)
        j41 = (yb - yu) / (bu *bu)
        j42 = (xb - xu) / (bu *bu)

        # Calculate the k values for distances
        k1 = dist_au - au
        k2 = dist_bu - bu

        # Calculate the k values for angles
        k3 = math.radians(dms2dec(az_a)) - (math.atan2((xa - xu), (ya - yu)))
        k4 = math.radians(dms2dec(az_b)) - (math.atan2((xb - xu), (yb - yu)))

        # create the J and K matrices using the calculated values
        j = np.matrix([[j11, j12], [j21, j22], [j31, j32], [j41, j42]])
        k = np.matrix([[k1], [k2], [k3], [k4]])

        jt = j.transpose()  # transpose the matrix
        jtj = jt * w * j  # calculate the first part of the solution including the weight matrix

        jtj = np.linalg.inv(jtj)  # get the inverse of this

        # X = inverse(Jt * W * J) * (Jt * W * K) <- this is the least squares solution equation
        x = jtj * (jt * w * k)  # solve for X

        xdiff = x[0, 0]  # get the change in X
        ydiff = x[1, 0]  # get the change in Y

        xu = xu + xdiff  # add the change to the starting x coord
        yu = yu + ydiff  # add the change to the starting y coord

        # if the new adjustment is smaller than 1mm then break out of the loop and finish least squares adjustment
        if math.fabs(xdiff) < 0.001 and math.fabs(ydiff) < 0.001:
            v = (j * x) - k  # variance matrix
            break
        cnt = cnt + 1


    return xu, yu, v, cnt
