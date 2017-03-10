import PtBCh5

# --------------------
# Input Data
# --------------------
navigationrestriction = 'unrestricted navigation'
dredgeractivity = 'dredging8'
L = 117.564
B = 24
cb = 0.85
T = 7
D = 9.8
servicespeed = 14
t1 = T
loadcase = 'a+'

# --------------------
# Input data required for the hopper
# --------------------
delta = 2
highest_weir_level = 8.416

# --------------------
# Navigation Coefficients
# --------------------
n = PtBCh5.navigation_coefficients('n', navigationrestriction)
if dredgeractivity == 'dredging8':
    n = 1 / 3
if dredgeractivity == 'dredging15':
    n = 2 / 3
if dredgeractivity == 'dredging15+':
    n = 1

n1 = PtBCh5.navigation_coefficients('n1', navigationrestriction)
C = PtBCh5.waveparameterc(L)
H = PtBCh5.waveparameterh(L)