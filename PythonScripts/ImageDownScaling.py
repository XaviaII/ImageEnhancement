import os
from PIL import Image

input_dir = '../04_Biggest_50/temp/00'
output_dir_donwlscaled = '../04_Biggest_50/tt'
output_dir_ground_truth = '../04_Biggest_50/temp/00_Original_4x'

factor = 4

# Funktion zum Verkleinern eines Bildes
def resize_image(input_path, output_path):
    with Image.open(input_path) as img:
        width, height = img.size
        new_size = (width // factor, height // factor)
        resized_img = img.resize(new_size)
        resized_img.save(output_path)

def ground_truth_image(input_path, output_path):
    with Image.open(input_path) as img:
        width, height = img.size
        new_size = (((width // factor) * factor) * factor, ((height // factor) * factor) * factor)
        resized_img = img.resize(new_size)
        resized_img.save(output_path)

# Funktion zum Durchlaufen der Ordnerstruktur und Verkleinern der Bilder
def process_folder(input_folder, output_folder_scaled, output_folder_ground_truth):
    for root, dirs, files in os.walk(input_folder):
        # Erstelle den entsprechenden Ausgabeordner in der Ausgabeordnerstruktur
        relative_path = os.path.relpath(root, input_folder)
        # Erstelle Ordner Stuktur für die low res Images
        output_subfolder_scaled = os.path.join(output_folder_scaled, relative_path)
        os.makedirs(output_subfolder_scaled, exist_ok=True)
        # Erstelle Ordner Struktur für die Ground Truth Images
        output_subfolder_ground_truth = os.path.join(output_folder_ground_truth, relative_path)
        os.makedirs(output_subfolder_ground_truth, exist_ok=True)

        # Verarbeite alle Dateien im aktuellen Ordner
        for file in files:
            file_path = os.path.join(root, file)
            # Downscale
            #output_file_path_scaled = os.path.join(output_subfolder_scaled, file)
            #resize_image(file_path, output_file_path_scaled)
            print("Verkleinert:", file_path)

            # Ground Truth
            output_file_path_ground_truth = os.path.join(output_subfolder_ground_truth, file)
            ground_truth_image(file_path, output_file_path_ground_truth)
            #print("GrundTruth:", file_path)


# Starte den Vorgang
process_folder(input_dir, output_dir_donwlscaled, output_dir_ground_truth)
