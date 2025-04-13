
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math

from constants import *

def connect(filepath="database.db"):
    # connect to database 
    db_path = os.path.join(filepath)
    conn = sqlite3.connect(db_path)
    
    # cursor object 
    return conn.cursor(), conn
    
# Close Connection to Database
def close_connection(conn):
    return conn.close()
    
def convert_to_rgb(lab_color):
    lab_array = np.array([[lab_color]], dtype=np.float64)
    rgb_array = lab2rgb(lab_array).squeeze()
    return np.clip(rgb_array * 255, 0, 255).astype(int)

def f(t):
    if t > 0.008856:
        return t ** (1/3.0)
    else:
        return 7.787 * t + 16/116.0
    
def xyz_to_lab(X, Y, Z, Xn=95.047, Yn=100, Zn=108.88):
    fx = f(X / Xn)
    fy = f(Y / Yn)
    fz = f(Z / Zn)
    
    L = 116 * fy - 16
    a = 500 * (fx - fy)
    b = 200 * (fy - fz)
    
    return L, a, b

def calculate_color_differences(df, lab_values, target_lab):
    # Convert to NumPy arrays
    lab_values = df[['L', 'a', 'b']].values.astype(float) 
    target_array = np.array(target_lab).reshape(1, 3) 

    # Compute deltaE for all rows
    deltaE = deltaE_ciede2000(lab_values, target_array)
    
    df['deltaE'] = deltaE
    return df.sort_values(by='deltaE')

def classify_mst_category(target_lab):
    min_de = float('inf')
    closest_category = 0
    for category, lab in MST_REF.items():
        current_de = deltaE_ciede2000([target_lab], [lab]).item()
        if current_de < min_de:
            min_de = current_de
            closest_category = category
    return closest_category, min_de

def load_data(category, file="cielab_data.npy"):
    data = np.load(file)

    columns = ['cielab_id', 'shade_id', 'red', 'green', 'blue', 
              'L', 'a', 'b', 'monk_category']
    df = pd.DataFrame(data, columns=columns)

    # return rows where category = target category
    if category is not None:
        df = df[df['monk_category'] == category]

    lab_values = df[['L', 'a', 'b']].to_numpy()
    
    return df, lab_values