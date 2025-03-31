import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math


def connect(filepath="database.db"):
    script_dir = os.path.dirname(__file__)
    
    db_path = os.path.abspath(os.path.join(script_dir, os.pardir, filepath))
    
    print("Database Path:", db_path)
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database file not found at: {db_path}")
    
    conn = sqlite3.connect(db_path)
    return conn.cursor(), conn
    
# Close Connection to Database
def close_connection(conn):
    return conn.close()
    
def convert_to_rgb(lab_color):
    lab_array = np.array([[lab_color]], dtype=np.float64)
    rgb_array = lab2rgb(lab_array).squeeze()
    return np.clip(rgb_array * 255, 0, 255).astype(int)

def get_input():
    while True:
        try:
            xyz_input = input("Enter XYZ color values (X, Y, Z): ")
            x, y, z = map(float, xyz_input.split(','))
            # Convert XYZ to LAB
            l, a, b = xyz_to_lab(x, y, z)
            # Validate LAB range
            if not (0 <= l <= 100 and -128 <= a <= 127 and -128 <= b <= 127):
                raise ValueError("Converted LAB values out of range")
            return (l, a, b)
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

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


def display_colors(rgb_values, titles):

    n_cols = 5
    n_rows = (len(rgb_values) + n_cols - 1) // n_cols  
    
    plt.figure(figsize=(n_cols * 3, n_rows * 3))  
    
    for i, (rgb, title) in enumerate(zip(rgb_values, titles)):
        color_block = np.ones((100, 100, 3)) * (np.array(rgb) / 255.0)

        plt.subplot(n_rows, n_cols, i + 1)
        plt.imshow(color_block)
        plt.title(title, pad=10, fontsize=8)
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

def calculate_color_differences(df, lab_values, target):
    target_array = np.array(target).reshape(1, -1)
    df['deltaE'] = deltaE_ciede2000(lab_values, target_array)
    return df.sort_values(by='deltaE')