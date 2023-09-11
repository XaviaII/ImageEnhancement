import cv2
import os
import Comparison as comparison

model = 'Upscayl'
filename = 'rum-09_right'
bbox = 'bbox_7'

# Pfad zum Ordner mit den Bildern
input_folder = f'../03_OriginalUpscale/{model}/{filename}/{bbox}'
input_ref_folder = f'../03_OriginalUpscale/00_Original_4x/{filename}/{bbox}'

def calculate_average_sharpness(input_folder, input_ref_folder):
    sharpness_values = []
    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):  # Passe die Dateiendungen an
            image_path = os.path.join(input_folder, filename)
            ref_image = os.path.join(input_ref_folder, filename)


            sharpness = comparison.calculate_sharpness(ref_image, image_path)
            print(f'{str(filename)}: {sharpness}')
            sharpness_values.append(sharpness)

    if sharpness_values:
        average_sharpness = sum(sharpness_values) / len(sharpness_values)
        return round(average_sharpness, 2)
    else:
        return 0.0  # Wenn kein Bild im Ordner gefunden wurde


average_sharpness = calculate_average_sharpness(input_folder, input_ref_folder)
print("Durchschnittlicher Sharpness-Wert:", average_sharpness)
