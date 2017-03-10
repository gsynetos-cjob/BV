from ship_input_file import *
import PtBCh5
import PtDCh13
import pyAPDL
import numpy as np
from tkinter import filedialog
from tkinter import *
import pandas as pd


root = Tk()

def var_states():
    hull = var1.get()
    hopper = var2.get()
    deck = var3.get()

    if hull == 1:
        # Read the APDL output txt file.
        df = pyAPDL.read_apdl_hull_coordinates()

        # Add new columns for ps,pw,pt
        df['label'] = 'hull'
        df["ps"] = 0.0
        df["pw"] = 0.0
        df["pt"] = 0.0

        for index, row in df.iterrows():
            x = row['x']
            z = row['z']
            h1 = PtBCh5.ship_relative_motion_upright(x, cb, n, C, L, T, D, t1)

            if row['label'] == 'hull':
                ps = PtBCh5.sea_still_water_pressure(z, t1)
                df.set_value(index, 'ps', ps)

                pw = PtBCh5.sea_wave_pressure_sides_and_bottom(z, t1, loadcase, h1, L, D)
                df.set_value(index, 'pw', pw)
                df.set_value(index, 'pt', (ps + 1.2 * pw))

        df.loc[:,'ps'] *= 1000
        final_df = df[['ID', 'ps']]
        # print(final_df)

        # --------------------
        # Save As
        # --------------------

        df.to_csv('pressures_on_shell_elements.csv')

        root = Tk()
        root.filename = filedialog.asksaveasfilename(initialdir="/", title="Save As",
                                                     filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        filename_save_as = root.filename + '.txt'
        np.savetxt(filename_save_as, final_df.values, newline=('\r' + '\n'), fmt='%12.1f')
        df.to_csv(root.filename + 'excel.csv')

        # df.to_csv('pressures_on_shell_elements.csv', header=False, index=False, columns=('ID','pt'))
        # print(df)

    if hopper == 1:
        # Read the APDL output txt file.
        df = pyAPDL.read_apdl_hopper_coordinates()

        # Add new columns for ps,pw,pt
        df['label'] = 'hopper'
        df['alpha'] = 0.0
        df["ps"] = 0.0
        df["pw"] = 0.0
        df["pt"] = 0.0

        for index, row in df.iterrows():
            x = row['x']
            z = row['z']
            alpha = np.degrees(np.arccos(row['zdircos']))
            h1 = PtBCh5.ship_relative_motion_upright(x, cb, n, C, L, T, D, t1)

            if row['label'] == 'hopper':
                df.set_value(index,'alpha',alpha)
                delta1 = PtDCh13.delta1(delta, alpha)
                dd = highest_weir_level - z
                ps = PtDCh13.still_water_pressure_hopper_well(dd, delta1)
                df.set_value(index, 'ps', ps)
                df.set_value(index, 'pt', ps)
        df.loc[:, 'ps'] *= 1000 # pressure in BV rules is in kN/m^2 and is exported in N/m^2 for Ansys
        final_df = df[['ID', 'ps']]
        # print(final_df)

        # --------------------
        # Save As
        # --------------------

        df.to_csv('pressures_on_shell_elements.csv')

        root = Tk()
        root.filename = filedialog.asksaveasfilename(initialdir="/", title="Save As",
                                                     filetypes=(("txt files", "*.txt"), ("all files", "*.*")))

        filename_save_as = root.filename + '.txt'
        np.savetxt(filename_save_as, final_df.values, newline=('\r' + '\n'), fmt='%12.1f')
        df.to_csv(root.filename + 'excel.csv')

        # df.to_csv('pressures_on_shell_elements.csv', header=False, index=False, columns=('ID','pt'))
        # print(df)


Label(root, text="Select Area:").grid(row=0, sticky=W)
var1 = IntVar()
Checkbutton(root, text="Hull (Bottom & Sides)", variable=var1).grid(row=1, sticky=W)
var2 = IntVar()
Checkbutton(root, text="Hopper", variable=var2).grid(row=2, sticky=W)
var3 = IntVar()
Checkbutton(root, text="Exposed Decks (under construction)", variable=var3).grid(row=3, sticky=W, column= 0)

Button(root, text='Select File(s)', command=var_states).grid(row=4, sticky=W, pady=4)
Button(root, text='Quit', command=root.quit).grid(row=5, sticky=W, pady=4)


mainloop()