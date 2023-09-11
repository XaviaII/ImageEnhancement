import os
from PIL import Image, ImageOps
import subprocess

model = 'Upscayl'
filename = 'rum-09_right'
bbox = 'bbox_7'

# Pfad zum Ordner mit den Bildern
input_folder = f'../03_OriginalUpscale/{model}/{filename}/{bbox}'

# Pfad und Name der Ausgabevideodatei
output_folder = f'../04_Biggest_50/03_VideoSequence/{filename}/{bbox}/{model}'

# Liste der Bilddateien im Ordner
image_files = os.listdir(input_folder)

# Initialisiere die maximale Breite und Höhe mit 0
max_width, max_height = 0, 0

# Durchlaufe die Bilddateien und finde die größte Bildgröße
for image_file in image_files:
    # Pfade zu den Bildern erstellen
    image_path = os.path.join(input_folder, image_file)

    # Größe des aktuellen Bildes ermitteln
    image = Image.open(image_path)
    width, height = image.size

    # Aktualisiere die maximale Breite und Höhe, falls erforderlich
    if width > max_width:
        max_width = width
    if height > max_height:
        max_height = height

# Neue Bildgröße
new_size = (max_width, max_height)

# Durchlaufe die Bilddateien erneut und erweitere sie mit einem schwarzen Rand
for image_file in image_files:
    # Pfade zu den Bildern erstellen
    image_path = os.path.join(input_folder, image_file)

    # Bild öffnen und mit schwarzem Rand erweitern
    image = Image.open(image_path)
    resized_image = ImageOps.pad(image, new_size, color='black')

    # Berechne die Höhenänderung
    delta_height = max_height - image.height

    # Erstelle ein neues Bild mit dem schwarzen Rand oben und unten
    final_image = Image.new(image.mode, (max_width, max_height), color='black')
    final_image.paste(resized_image, (0, delta_height // 2))

    # Speichere das Bild mit erweiterter Größe
    final_image.save(os.path.join(output_folder, image_file))


