import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math
from helperFunctions import connect, convert_to_rgb, get_input
from helperFunctions import xyz_to_lab, display_colors, calculate_color_differences,close_connection

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
    # if category is not None:
    #     df = df[df['monk_category'] == category]

    lab_values = df[['L', 'a', 'b']].to_numpy()
    
    return df, lab_values
    

def getMatches():
    target_lab = get_input()
    
    mst_category, mst_de = classify_mst_category(target_lab)
    
    print(f"\nAnalyzing color matches for L: {target_lab[0]} a: {target_lab[1]} b: {target_lab[2]}")
    print(f"Closest MST Category: {mst_category} (ΔE: {mst_de:.2f})")

    df, lab_values = load_data(mst_category) 

    df_sorted = calculate_color_differences(df, lab_values, target_lab)
    threshold_matches = df_sorted[df_sorted['deltaE'] <= DELTA_E_THRESHOLD] # Delta E within threshold
    
    # print(f"Threshold Matches: {threshold_matches}")
    
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
    # print(combined_df[['type', 'shade_id', 'L', 'a', 'b', 'RGB', 'deltaE']].to_markdown(index=False))
    
    shade_ids = combined_df[combined_df['type'] == 'Match']['shade_id'].values
    delta_e = combined_df[combined_df['type'] == 'Match']['deltaE'].values
    
    return shade_ids, delta_e

def getProducts(shade_matches, delta_e, cursor_obj):
    product_matches = []
    delta = []
    delta_percentage = []
    for shade, de in zip(shade_matches, delta_e):

        statement = f''' 
        SELECT brands.brand_name, products.product_name, shades.shade_name
        FROM shades
        INNER JOIN products ON shades.product_id = products.product_id
        INNER JOIN brands ON products.brand_id = brands.brand_id
        WHERE shades.shade_id = {shade};
        '''
        cursor_obj.execute(statement)
        output = cursor_obj.fetchall()
        
        for row in output:
            product_matches.append(row)
            d = round((100 - de)/100 * 100,2)
            delta_percentage.append( str(d) + '%') 
            delta.append(de)
    
    df_product_matches = pd.DataFrame(product_matches, columns=['Brand', 'Product', 'Shade'])
    df_product_matches['Percent Match'] = delta_percentage 
    print(df_product_matches[['Brand', 'Product', 'Shade', 'Percent Match']].to_markdown(index=False))
    return

        
def main():

    cielab = []
    cursor_obj, conn = connect()

    statement = f''' 
    SELECT * 
    FROM cielab
    '''
    cursor_obj.execute(statement)

    output = cursor_obj.fetchall()

    for row in output:
        cielab.append(row)

    np.save('cielab_data.npy', cielab)
    conn.commit()

    shade_matches, delta_e = getMatches()

    getProducts(shade_matches, delta_e, cursor_obj)

    close_connection(conn)
    return


if __name__ == "__main__":
    main()
