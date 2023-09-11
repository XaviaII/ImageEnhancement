import os
from PIL import Image
import matplotlib.pyplot as plt



def get_image_sizes(folder_path):
    total_files = 0
    completed_files = 0

    for root, dirs, files in os.walk(folder_path):
        total_files += len(files)


    sizes = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                image_path = os.path.join(root, file)
                with Image.open(image_path) as img:
                    width, height = img.size
                sizes.append((width, height))

            completed_files += 1
            percent_completed = (completed_files / total_files) * 100
            print(f'Progress: {percent_completed:.2f}%')
    return sizes


def plot_image_sizes(folder_path):
    sizes = get_image_sizes(folder_path)
    widths, heights = zip(*sizes)

    plt.figure(figsize=(10, 6))
    plt.scatter(widths, heights, alpha=0.5)
    plt.xlabel('Width')
    plt.ylabel('Height')
    plt.title('Image Sizes Distribution')
    plt.grid(True)
    plt.show()


# Beispielaufruf
folder_path = '../02_ImagesUpscale/01_LowRes_Images'

plot_image_sizes(folder_path)