import numpy as np
from skimage.color import rgb2lab, deltaE_ciede2000

def hex2lab(hex_color):
    hex_color = hex_color.lstrip('#')
    rgb = np.array([
        int(hex_color[i:i+2], 16) / 255.0 
        for i in (0, 2, 4)
    ], dtype=np.float64)
    rgb_reshaped = rgb.reshape((1, 1, 3))
    lab = rgb2lab(rgb_reshaped)
    return lab[0, 0]


if __name__ == "__main__":

    while True:
        try:
            expected_hex = input("Enter expected hex color (e.g. #ff0000): ").strip()
            measured_hex = input("Enter measured hex color (e.g. #cc0000): ").strip()
            
            expected_lab = hex2lab(expected_hex)
            measured_lab = hex2lab(measured_hex)
            
            delta_e = deltaE_ciede2000(expected_lab, measured_lab)
            print(f"DeltaE (CIEDE2000) difference: {delta_e:.2f}\n")
            print(f"Percent Match: {round((100 - delta_e) / 100 * 100, 2)}")
        except KeyboardInterrupt:
            print("\nExiting.")
            break
