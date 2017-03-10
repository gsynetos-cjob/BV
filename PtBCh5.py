from math import sqrt, exp, pi

# ------------------------
# CHAPTER 5
# ------------------------

# ------------------------
# Section 1
# ------------------------


def navigation_coefficients (coefficient, navigation_notation):
    """Calculates the navigation coefficients n and n1 as per NR467 BV,PtB,Ch5,Sec1

       Input:
       type: Navigation Coefficient (n or n1)
       navigation notation: 'unrestricted navigation'
                            'summer zone'
                            'tropical zone'
                            'coastal zone'
                            'sheltered area'
    """

    if coefficient == 'n':
        dict = {'unrestricted navigation': 1, 'summer zone': 0.9, 'tropical zone': 0.8, 'coastal zone': 0.8, 'sheltered area': 0.65}
        return dict[navigation_notation]
    if coefficient == 'n1':
        dict = {'unrestricted navigation': 1, 'summer zone': 0.95, 'tropical zone': 0.9, 'coastal zone': 0.9, 'sheltered area': 0.8}
        return dict[navigation_notation]

# ------------------------
# Section 2
# ------------------------


def waveparameterc(L):
    """Calculates the wave parameter C as per NR467 BV,PtB,Ch5,Sec2

       Input:
       L: Rule Lenght [m] """

    if 65 <= L < 90:
        return (118 - 0.36 * L) * (L / 1000)
    if 90 <= L < 300:
        return 10.75 - ((300-L) / 100) ** 1.5
    if 300 <= L <= 350:
        return 10.75
    if L > 350:
        return 10.75 - ((L-350) / 150) ** 1.5


def waveparameterh(L):
    """Calculates the wave parameter C as per NR467 BV,PtB,Ch5,Sec2

       Input:
       L: Rule Lenght [m] """
    return 8.13 - ((250 - 0.7 * L) / 125) ** 3

# ------------------------
# Section 3
# ------------------------


def ship_relative_motion_upright(x, cb, n, C, L, T, D, t1):

    """Calculates the reference value h1
    of the relative motion according to NR467 BV,PtB,Ch5,Sec3,[3.3]

    srm_u "Ship Relative Motion in upright condition"
    Input
    ------
    C_b : Block Coefficient
    n: navigation coeffecient as per NR467 BV,PtB,Ch5,Sec1,[2.6]
    C: Wave Parameter NR467 BV,PtB,Ch5,Sec2
    L: Rule Lenght [m]
    T: Design Draught [m]
    D: Depth [m]
    T1: Draught associated with each loading condition [m]

    Output
    -------
    h1: ship relative motion reference value"""

    h1_M = 0.42 * n * C * (cb + 0.7)
    if x == 0:
        if cb < 0.875:
            return 0.7 *((4.35 / sqrt(cb)) - 3.25) * h1_M
        return h1_M
    if x < 0.3 * L:
        h1_AE = 0.7 * ((4.35 / sqrt(cb)) - 3.25) * h1_M
        return h1_AE - ((h1_AE - h1_M) / 0.3) * (x/L)
    if x < 0.7 * L:
        limit = min(t1, D - 0.9 * T)
        return min(0.42 * n * C * (cb + 0.7), limit)
    if x < L:
        h1_FE = ((4.35 / sqrt(cb)) - 3.25) * h1_M
        return h1_M + ((h1_FE - h1_M) / 0.3)*((x / L)-0.7)
    return ((4.35 / sqrt(cb)) - 3.25) * h1_M



# ------------------------
# Section 5
# ------------------------


def sea_still_water_pressure(z, t1, rho=1.025, g=9.81):

    """Calculates the still water  sea pressure as per NR467 BV,PtB,Ch5,Sec5,[1]

    Input
    ------
    z: considered location [m]
    T1: Draught associated with each loading condition [m]
    rho: sea water density []
    g: gravity accelearation [m/s^2]

    Output
    -------
    ps: still water pressure in [kN/m^2]"""

    if z <= t1:
        return rho * g * (t1 - z)
    else:
        return 0


def sea_wave_pressure_sides_and_bottom(z, t1, loadcase, h1, L, D, rho=1.025, g=9.81):

    """ Calculates the wave sea pressure on bottom and sides according to NR467 BV,PtB,Ch5,Sec5,[2]

    Input
    ------
    z: considered location [m]
    T1: draught [m]
    loadcase: Load Case ('a+' , 'a-' , 'b' , 'c', 'd')
    L: Rule Length [m]
    h1: Reference Values of the ship relative motions in the upright ship condition, defined in Ch5,Sec3,[3.3]
    rho: sea water density [t/m^3]
    g: gravity acceleration [m/s^2]

    Output
    -------
    pw: sea wave pressure in [kN/m^2]
    """

    cf1 = cf1_combination_factor(loadcase)
    phi1 = 1
    phi2 = phi2_coefficient(L)

    if loadcase == 'a+':
        if z <= t1:
            return rho * g * cf1 * h1 * exp((-2 * pi * (t1 - z) / L))
        if t1 < z <= D:
            limit = 0.15 * phi1 * phi2 * L
            return max(rho * g * (t1 + h1 - z), limit)

    if loadcase == 'a-':
        if z <= t1:
            return max(-rho * g * h1 * exp((-2 * pi * (t1 - z) / L)), rho * g * (z - t1))
        if t1 < z <= D:
            return 0

    if loadcase == 'b':
        if z <= t1:
            return rho * g * cf1 *h1 * exp((-2 * pi * (t1 - z) / L))
        if t1 < z <= D:
            limit = 0.15 * phi1 * phi2_coefficient(L) * L
            return max(rho * g * (t1 + h1 - z), limit)


def sea_still_water_pressure_exposed_decks(L):
    phi1 = 1
    phi2 = phi2_coefficient(L)
    return 10 * phi1 * phi2

def sea_wave_pressure_exposed_decks(x, z, t1, loadcase, L, n, cb, servicespeed = 13):

    """ Calculates the wave sea pressure on exposed deck according to NR467 BV,PtB,Ch5,Sec5,[Tab4]

    Input
    ------
    x: x-coordinate [m]
    z: considered location [m]
    t1: draught [m]
    loadcase: Load Case ('a+' , 'a-' , 'b', 'c', 'd')
    L: Rule Length [m]
    servicespeed: maximum ahead service speed [kn] not less than 13
    n: navigation coefficient
    C_b: block coefficient
    h1: Reference Values of the ship relative motions in the upright ship condition, defined in Ch5,Sec3,[3.3]

    Output
    -------
    pw: sea wave pressure in exposed decks in [kN/m^2]
    """

    phi1 = 1
    phi2 = phi2_coefficient(L)
    v = max(servicespeed, 13)

    if loadcase == 'a+' or loadcase == 'b':
        if 0 <= x <= 0.5 * L:
            return 17.5 * n * phi1 * phi2
        if 0.5 * L < x < 0.75 * L:
            hf = h_formula(0.75 * L, L, v, cb, z, t1, loadcase)
            return (17.5 + ((19.6 * sqrt(hf) - 17.5) / 0.25) * ((x / L) - 0.5))* n * phi1 * phi2
        if 0.75 * L <= x <= L:
            h = h_formula(x, L, v, cb, z, t1, loadcase)
            return 19.6 * n * phi1 * phi2 * sqrt(h)

    if loadcase == 'a-':
        return 0


def phi2_coefficient(L):
    """ Calculates the phi 2 coefficient, used for the calculation of the wave pressure NR467 BV,PtB,Ch5,Sec5,[Tab4]

        Input
        ------
        L: Rule Length [m]

        Output
        -------
        phi2
    """

    if 0 < L < 120:
        return L / 120
    if L >= 120:
        return 1


def cf1_combination_factor(loadcase):
    if loadcase == 'a+' or loadcase == 'a-':
        return 1
    if loadcase == 'b':
        return 0.5


def h_formula(x, L, v, cb, z, t1, loadcase):
    return max (cf1_combination_factor(loadcase) *  ((2.66 * ((x / L) - 0.7) ** 2 ) + 0.14) * sqrt((v * L ) / cb) - (z - t1), 0.8)
