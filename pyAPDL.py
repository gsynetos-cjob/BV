import pandas as pd
import tkinter as tk
from tkinter import filedialog

# --------------------
# Read ADPL txt file  with shell coordinates and Apply Sea pressure on shell and decks and Spoil Pressure on Hopper
# --------------------

def read_apdl_hull_coordinates(*args):
    """Reads the APDL output txt file which contains the shell element ID and coordinates and returns a pd dataframe

      Input
      -----
      *.txt file (if the filename is not given then opens the browser)

      Output:
      -------
      Panda Dataframe
      """

    filename = str(*args)+'.txt'
    if filename == '.txt':
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()

    df = pd.read_fwf(filename, colspecs=[(0,12),(12,24),(24,36),(36,48)], names=['ID','x','y','z'])

    return df

def read_apdl_hopper_coordinates(*args):
    """Reads the APDL output txt file which contains the hoper's element ID, x,y,z coordinates AND the z direction
        cosine (which is required in order to calculate the angle alpha for the pressure in the hopper
        and returns a pd dataframe

      Input
      -----
      *.txt file (if the filename is not given then opens the browser)

      Output:
      -------
      Panda Dataframe
      """

    filename = str(*args)+'.txt'
    if filename == '.txt':
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()

    df = pd.read_fwf(filename, colspecs=[(0,12),(12,24),(24,36),(36,48),(48,60)], names=['ID','x','y','z','zdircos'])

    return df

