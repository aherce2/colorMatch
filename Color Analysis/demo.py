import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage.color import lab2rgb, deltaE_ciede2000
import sqlite3
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from skimage.color import lab2rgb, deltaE_ciede2000



TARGET_LAB = (37.807,28.676,36.338)
NUM_CLUSTERS = 10
TOP_MATCHES = 10
DELTA_E_THRESHOLD = 1.5

# Connect to Database
def connect(filepath="database.db"):
    # connect to database 
    db_path = os.path.join(filepath)
    print("Database Path:", db_path)
    conn = sqlite3.connect(db_path)
    
    # cursor object 
    return conn.cursor(), conn
    
def convert_to_rgb(lab_color):
    lab_array = np.array([[lab_color]], dtype=np.float64)
    rgb_array = lab2rgb(lab_array).squeeze()
    return np.clip(rgb_array * 255, 0, 255).astype(int)

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

def kmeans_clustering(lab_values, n_clusters):
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    return kmeans.fit_predict(lab_values)

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

def create_visualizations(df, target, top_matches):
    fig, ax = plt.subplots(2, 1, figsize=(12, 12))
    
    # Delta E plot
    sc1 = ax[0].scatter(df['a'], df['b'], c=df['deltaE'], cmap='plasma', s=50, alpha=0.8)
    ax[0].scatter(target[1], target[2], color='red', s=200, edgecolor='black', marker='*')
    ax[0].scatter(top_matches['a'], top_matches['b'], color='lime', s=100, edgecolor='black', linewidth=1)
    ax[0].set_title('Color Differences (ΔE 2000) from Target')
    ax[0].set_xlabel('a* (Green-Red)')
    ax[0].set_ylabel('b* (Blue-Yellow)')

    cbar = plt.colorbar(sc1, ax=ax[0], orientation='vertical')
    cbar.set_label('Delta E')
    cbar.ax.invert_yaxis()  # Reverse the color bar
    
    # K-means plot
    clusters = df['cluster'].unique()
    cluster_colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))
    for cluster, color in zip(clusters, cluster_colors):
        cluster_data = df[df['cluster'] == cluster]
        ax[1].scatter(cluster_data['a'], cluster_data['b'], color=color, s=50, alpha=0.7)
    ax[1].scatter(target[1], target[2], color='red', s=200, edgecolor='black', marker='*')
    ax[1].set_title(f'K-means Clustering (k={NUM_CLUSTERS}) of Skin Tones')
    ax[1].set_xlabel('a* (Green-Red)')
    ax[1].set_ylabel('b* (Blue-Yellow)')
    
    plt.tight_layout()
    plt.show()

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


def load_data(file="cielab_data.npy"):
    data = np.load(file)
    
    # Extract L, a, and b values from each row (tuple)
    lab_values = data[:, 2:5]  

    columns = ['id', 'shade_id', 'L', 'a', 'b', 'category']
    df = pd.DataFrame(data, columns=columns)
    
    return df, lab_values

def getMatches():
    target_lab = get_input()

    print(f"\nAnalyzing color matches for L: {target_lab[0]} a: {target_lab[1]} b: {target_lab[2]}")
    
    df, lab_values = load_data() 
    
    df_sorted = calculate_color_differences(df, lab_values, target_lab)
    top_matches = df_sorted.head(TOP_MATCHES) 
    
    df['cluster'] = kmeans_clustering(lab_values, NUM_CLUSTERS)
    
    create_visualizations(df, target_lab, top_matches)
    
    target_df = pd.DataFrame([{
        'id': None, 'shade_id': None,  
        'L': target_lab[0], 'a': target_lab[1], 'b': target_lab[2],
        'deltaE': 0, 'type': 'Target'
    }])
    
    matches_df = top_matches[['id', 'shade_id', 'L', 'a', 'b', 'deltaE']].copy()
    matches_df['type'] = 'Match'
    
    combined_df = pd.concat([target_df, matches_df], ignore_index=True)
    
    combined_df['RGB'] = combined_df.apply(lambda row: convert_to_rgb((row['L'], row['a'], row['b'])), axis=1)
    
    rgb_values = [row for row in combined_df['RGB']]
    titles = [f"{row['type']} (Shade ID: {row['shade_id']})\nL: {row['L']:.2f} a: {row['a']:.2f} b: {row['b']:.2f}\nΔE: {row['deltaE']:.2f}" 
              for _, row in combined_df.iterrows()]
    
    display_colors(rgb_values, titles)
    
    print("\nColor Comparison Table:")
    print(combined_df[['type', 'shade_id', 'L', 'a', 'b', 'RGB', 'deltaE']].to_markdown(index=False))


    shade_ids = combined_df[combined_df['type'] == 'Match']['shade_id'].values
    delta_e = combined_df[combined_df['type'] == 'Match']['deltaE'].values
    return shade_ids, delta_e

# Close Connection to Database
def close_connection(conn):
    return conn.close()

def getProducts(shade_matches, delta_e, cursor_obj):
    product_matches = []
    delta = []

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
            delta.append(de)
    
    df_product_matches = pd.DataFrame(product_matches, columns=['Brand', 'Product', 'Shade'])
    df_product_matches['Delta E'] = delta 
    print(df_product_matches[['Brand', 'Product', 'Shade', 'Delta E']].to_markdown(index=False))
    return

            

def main():

    shades = ['very_fair', 'fair', 'medium', 'monk', 'olive', 'brown']

    cielab = []
    cursor_obj, conn = connect()

    for shade in shades:
        statement = f''' 
        SELECT * 
        FROM {shade}
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



