'''
Fetch the products based on return data

When Lab Values are sent call function to get data and display to front end

'''
import sqlite3
import os
import math
from Helper_Functions.analyzeData import *
from constants import socketio

def getMatches(target_lab):

    mst_category = classify_mst_category(target_lab)

    # Broadcast User's Monk Category
    socketio.emit('monk_category', {'monk_category': mst_category})
    print(f"Monk Category: {mst_category}")
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

            
def analyzeInput(target_lab):
    
    cursor_obj, conn = connect()
    shade_matches, delta_e = getMatches(target_lab)
    products = getProducts(shade_matches, delta_e, cursor_obj)
    close_connection(conn)
    # Broadcast User's measured Shade 
    socketio.emit('target_lab', {'target': convert_to_rgb(target_lab)})
    socketio.emit('lab_products', {'products': products}) # Broadcast products
    return products

