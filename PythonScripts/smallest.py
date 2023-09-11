import os
from PIL import Image

def find_smallest_largest_image(directory):
    min_size = float('inf')
    max_size = 0
    min_path = ''
    max_path = ''

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    width, height = img.size
                    image_size = width * height

                if image_size < min_size:
                    min_size = image_size
                    min_path = image_path

                if image_size > max_size:
                    max_size = image_size
                    max_path = image_path

    return min_path, max_path

# Beispielaufruf
directory_path = '../02_ImagesUpscale/00_GroundTruth_Images'

smallest_image_path, largest_image_path = find_smallest_largest_image(directory_path)
print("Kleinste Bildgröße:", smallest_image_path)
print("Größte Bildgröße:", largest_image_path)