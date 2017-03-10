from math import sin
import numpy as np

# ------------------------
# CHAPTER 13
# ------------------------

def delta(pd, vd):
    """Calculates the specific gravity of the mixture of sea water and spoil

    Input
    -----
    pd: Maximum mass, of the spoil contained in the hopper space [t]
    vd: Volume of the hopper space limited to the highest weir level [m^3]

    Output
    ------
    delta
    """
    return pd / vd

# ------------------------
# Section 2
# ------------------------


def delta1(delta, alpha=0):
    """Calculates the delta1 value depending on the density of the spoil"""

    if delta < 1.4:
        return delta
    if delta >= 1.4:
        return delta + (1.4 - delta) * sin(np.radians(alpha)) ** 2


def still_water_pressure_hopper_well(dd, delta1, g=9.81):

    """ Calculates the still water pressure as per NR467 BV,PtD,Ch13,Sec2,[3.5.1]

    The still water pressure to be used in connection with inertial pressure in NR467 BV,PtD,Ch13,Sec2,[3.5.2]

    Input
    -----
    delta1:
    g:  gravity acceleration [m/s^2]
    dd: vertical distance from the calculation point to the highest weir level with the corresponding specific gravity
        of the mixture of sea water and spoil [m]
    alpha: angle between the horizontal plane and the surface of the hull structure to which the calculation point
        belongs [deg]

    Output
    ------
    ps: still water pressure [kN/m^2]
    """

    return max(g * delta1 * dd, 11)


def inertia_pressure_hopper_well():
    """ Calculates the inertial pressure as per NR467 BV,PtD,Ch13,Sec2,[3.5.2],Tab6

    Input
    -----
    loadcase: a+, a-, b, c, d
    delta1: coefficient related to delta and angle alhpa
    dd: vertical distance from the calculation point to the highest weir level with the corresponding specific gravity
        of the mixture of sea water and spoil [m]

    Output
    ------
    ps: still water pressure [kN/m^2]

    """

    if loadcase == 'a+' or 'a-':
        return 0
    if loadcase == 'b':
        #to be calculated
        pass
    if loadcase == 'c':
        #to be calculated
        pass
    if loadcase == 'd':
        #to be calulated
        pass
