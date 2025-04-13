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
from Helper_Functions.analyzeData import *

# def getMatches(target_lab):
#     # target_lab = get_input()
#     # target_lab = get_ble_lab()
    
#     # Hardcode for frontend integration/debugging -> Return target lab + mst category to frontend later
#     # target_lab = [66.611,17.184,39.107]

#     mst_category, mst_de = classify_mst_category(target_lab)

#     df, lab_values = load_data(mst_category) 

#     df_sorted = calculate_color_differences(df, lab_values, target_lab)
#     threshold_matches = df_sorted[df_sorted['deltaE'] <= DELTA_E_THRESHOLD] # Delta E within threshold
    
    
#     target_df = pd.DataFrame([{
#         'id': None, 'shade_id': None,  
#         'L': target_lab[0], 'a': target_lab[1], 'b': target_lab[2],
#         'deltaE': 0, 'type': 'Target'
#     }])
    
#     matches_df = threshold_matches[['cielab_id', 'shade_id', 'L', 'a', 'b', 'deltaE']].copy()
#     matches_df['type'] = 'Match'
    
#     combined_df = pd.concat([target_df, matches_df], ignore_index=True)
#     combined_df['RGB'] = combined_df.apply(lambda row: convert_to_rgb((row['L'], row['a'], row['b'])), axis=1)

    
#     shade_ids = combined_df[combined_df['type'] == 'Match']['shade_id'].values
#     delta_e = combined_df[combined_df['type'] == 'Match']['deltaE'].values
    
#     return shade_ids, delta_e

def getMatches(target_lab):
    
    mst_category, mst_de = classify_mst_category(target_lab)
    df, lab_values = load_data(mst_category)
    df_sorted = calculate_color_differences(df, lab_values, target_lab)
    
    # Get matches within threshold
    threshold_matches = df_sorted[df_sorted['deltaE'] <= DELTA_E_THRESHOLD]
    
    # Extract directly from DataFrame columns
    shade_ids = threshold_matches['shade_id'].tolist()
    delta_e = threshold_matches['deltaE'].tolist()
    
    return shade_ids, delta_e

def getProducts(shade_matches, delta_e, cursor_obj):
    product_dict = []


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
    print(product_dict)
    return product_dict

            
def getUserData(target_lab):
    
    cursor_obj, conn = connect()

    shade_matches, delta_e = getMatches(target_lab)

    products = getProducts(shade_matches, delta_e, cursor_obj)

    close_connection(conn)
    
    return products

