import pandas as pd
import PtBCh5
import PtDCh13

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
delta = 1.3
highest_weir_level = 12


# --------------------
# Read Multiframe csv file and Apply Sea pressure on shell and decks and Spoil Pressure on Hopper
# --------------------

multiframe_joints_column_names = ['joint', 'label', 'x', 'z', 'y', 'type', 'xxx', 'xxx', 'xxx']
joints_df = pd.read_csv('multiframepoints.csv', names=multiframe_joints_column_names,
                        usecols=['joint', 'label', 'x', 'y', 'z'])
joints_df["ps"]= 0
joints_df["pw"]= 0
joints_df["pt"]= 0


for index, row in joints_df.iterrows():
    x = row['x']
    z = row['z']

    n = PtBCh5.navigationcoefficients('n', navigationrestriction)
    if dredgeractivity == 'dredging8':
        n = 1 / 3
    if dredgeractivity == 'dredging15':
        n = 2 / 3
    if dredgeractivity == 'dredging15+':
        n = 1

    n1 = PtBCh5.navigationcoefficients('n1', navigationrestriction)
    C = PtBCh5.waveparameterc(L)
    H = PtBCh5.waveparameterh(L)
    h1 = PtBCh5.shiprelativemotionupright(x, cb, n, C, L, T, D, t1)

    if row['label'] == 'shell':
        ps = PtBCh5.seastillwaterpressure(z, t1)
        joints_df.set_value(index, 'ps', ps)

        pw = PtBCh5.seawavepressuresidesandbottom(z, t1, loadcase, h1, L, D)
        joints_df.set_value(index, 'pw', pw)
        joints_df.set_value(index, 'pt', ps + 1.2 * pw)
        # print('ps=', ps,'pw=', pw,'ptotal=', ps + 1.2 * pw)

    if row['label'] == 'deck':
        psdeck = PtBCh5.seastillwaterpressureexposeddecks(L)
        joints_df.set_value(index, 'ps', psdeck)
        #print('psdeck=', psdeck)
        pwdeck = PtBCh5.seawavepressureexposeddecks(x, z, t1, loadcase, L, n, cb, servicespeed)
        joints_df.set_value(index, 'pw', pwdeck)
        joints_df.set_value(index, 'pt', psdeck + 1.2 * pwdeck)
        #print('pwdeck=', pwdeck)

    if row['label'] == 'hopper':
        delta1 = PtDCh13.delta1(delta)
        dd = highest_weir_level - z
        ps = PtDCh13.still_water_pressure_hopper_well(dd, delta1)
        joints_df.set_value(index, 'ps', ps)
        joints_df.set_value(index, 'pt', ps)


# print(joints_df)
joints_df.to_csv('pressures_on_joints.csv')

multiframe_member_geometry_column_names = ['member', 'label', 'joint1', 'joint2', 'length', 'slope', 'offset axes',
                                           'x off', 'y off', 'z off', 'x off2', 'y off2', 'z off2']
member_geometry_df = pd.read_csv('multiframe_member_geometry.csv', names=multiframe_member_geometry_column_names,
                                 usecols=['member', 'label','joint1', 'joint2'])



member_geometry_df["joint1_pt"]= 0
member_geometry_df["joint2_pt"]= 0
# print(member_geometry_df)

df1 = joints_df
df1.set_value(0, 'joint', 1)
print(df1)

df2 = member_geometry_df
df2.set_value(0, 'member', 1)
print(df2)


d = df1.set_index('joint')['pt'].to_dict()
d = {int(k):int(v) for k,v in d.items()}
df2['joint1_pt'] = df2['joint1'].map(d)
df2['joint2_pt'] = df2['joint2'].map(d)
print (df2)
df2.to_csv('pandas_member_loads.csv')