'''
Fetch the products based on return data

When Lab Values are sent call function to get data and display to front end

'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math


DELTA_E_THRESHOLD = 1.75

# MST Reference Colors (L, a, b values)
MST_REF = {
    1: (94.211, 1.503, 5.422),
    2: (92.275, 2.061, 7.28),
    3: (93.091, 0.216, 14.205),
    4: (87.573, 0.459, 17.748),
    5: (77.902, 3.471, 23.136),
    6: (55.142, 7.783, 26.74),
    7: (42.47, 12.325, 20.53),
    8: (30.678, 11.667, 13.335),
    9: (21.069, 2.69, 5.964),
    10: (14.61, 1.482, 3.525)
}


def connect(filepath="database.db"):
    # connect to database 
    db_path = os.path.join(filepath)
    print("Database Path:", db_path)
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
        print(current_de)
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

def getMatches():
    # target_lab = get_input()
    # target_lab = get_ble_lab()
    
    # Hardcode for frontend integration/debugging
    target_lab = [66.611,17.184,39.107]

    print(target_lab)
    mst_category, mst_de = classify_mst_category(target_lab)
    
    print(f"\nAnalyzing color matches for L: {target_lab[0]} a: {target_lab[1]} b: {target_lab[2]}")
    print(f"Closest MST Category: {mst_category} (ΔE: {mst_de:.2f})")
    
    df, lab_values = load_data(mst_category) 

    df_sorted = calculate_color_differences(df, lab_values, target_lab)
    threshold_matches = df_sorted[df_sorted['deltaE'] <= DELTA_E_THRESHOLD] # Delta E within threshold
    
    
    target_df = pd.DataFrame([{
        'id': None, 'shade_id': None,  
        'L': target_lab[0], 'a': target_lab[1], 'b': target_lab[2],
        'deltaE': 0, 'type': 'Target'
    }])
    
    matches_df = threshold_matches[['cielab_id', 'shade_id', 'L', 'a', 'b', 'deltaE']].copy()
    matches_df['type'] = 'Match'
    
    combined_df = pd.concat([target_df, matches_df], ignore_index=True)
    combined_df['RGB'] = combined_df.apply(lambda row: convert_to_rgb((row['L'], row['a'], row['b'])), axis=1)
    
    print("\nColor Comparison Table:")
    print(combined_df[['type', 'shade_id', 'L', 'a', 'b', 'RGB', 'deltaE']].to_markdown(index=False))
    
    shade_ids = combined_df[combined_df['type'] == 'Match']['shade_id'].values
    delta_e = combined_df[combined_df['type'] == 'Match']['deltaE'].values
    
    return target_lab, mst_category, shade_ids, delta_e

def getProducts(shade_matches, delta_e, cursor_obj):
    product_dict = []
    delta = []
    delta_percentage = []
    for shade, de in zip(shade_matches, delta_e):
        statement = f''' 
        SELECT shades.shade_id, brands.brand_name, products.product_name, shades.shade_name, shades.hex
        FROM shades
        INNER JOIN products ON shades.product_id = products.product_id
        INNER JOIN brands ON products.brand_id = brands.brand_id
        WHERE shades.shade_id = {shade};
        '''
        cursor_obj.execute(statement)
        output = cursor_obj.fetchall()
        
        product_matches = []
        #save and return as a dictonary
        for row in output:
            shade_id, brand, product, shade_name, hex_value= row
            percent_match = round((100 - de) / 100 * 100, 2)
            product_dict.append({
                "id": shade_id,
                "brand": brand,
                "product": product,
                "shade": shade_name,
                "hex": hex_value,
                "percent_match": f"{percent_match}%"
            })

    return product_dict

            
def getUserData():
    
    cielab = []
    cursor_obj, conn = connect()

    # statement = f''' 
    # SELECT * 
    # FROM cielab
    # '''
    # cursor_obj.execute(statement)

    # output = cursor_obj.fetchall()

    # for row in output:
    #     cielab.append(row)

    # np.save('cielab_data.npy', cielab)
    # conn.commit()

    target_lab, mst_category, shade_matches, delta_e = getMatches()

    products = getProducts(shade_matches, delta_e, cursor_obj)

    close_connection(conn)
    
    return products
