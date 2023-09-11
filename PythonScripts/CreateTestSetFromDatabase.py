import os
import random
import shutil

def move_images(root_folder, output_folder):
    for foldername, subfolders, filenames in os.walk(root_folder):
        image_files = [filename for filename in filenames if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        num_images = len(image_files)
        num_to_move = int(num_images * 0.2)  # 20% der Bilder

        if num_to_move > 0:
            # Erstelle den Zielordner im Ausgabepfad
            relative_path = os.path.relpath(foldername, root_folder)
            destination_folder = os.path.join(output_folder, relative_path)
            os.makedirs(destination_folder, exist_ok=True)

            # Wähle zufällige Bilder aus
            selected_images = random.sample(image_files, num_to_move)

            # Verschiebe die ausgewählten Bilder
            for image in selected_images:
                source_path = os.path.join(foldername, image)
                destination_path = os.path.join(destination_folder, image)
                shutil.move(source_path, destination_path)
                print(f"Verschoben: {source_path} -> {destination_path}")

# Beispielaufruf:
root_folder = '../Upscaler/Real_ESRGAN/datasets/finetune'  # Gib hier den Pfad zu deinem Root-Ordner an
output_folder = '../Upscaler/Real_ESRGAN/datasets/finetune_testdata'  # Gib hier den Pfad zum Ausgabeverzeichnis an

move_images(root_folder, output_folder)