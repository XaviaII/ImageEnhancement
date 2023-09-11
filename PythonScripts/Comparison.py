import os
import math
import cv2
import imutils
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

import torch
import torchvision.transforms as transforms

import imagehash
import distance
from PIL import Image

from skimage.metrics import structural_similarity
from torchmetrics.image.lpip import LearnedPerceptualImagePatchSimilarity
from dom import DOM


import BlindMetricModule.brisque.brisque as brisque
import BlindMetricModule.niqe.niqe as niqe
import BlindMetricModule.piqe.piqe as piqe
import BlindMetricModule.MetaIQA.model as MetaIQA
import BlindMetricModule.RankIQA.model as RankIQA

round_to = 2

def convert_normalize(image_path):
    image = Image.open(image_path).convert('RGB')

    # Definiere die Transformationen
    transform = transforms.Compose([
        transforms.Resize((64, 64)),  # Ändere die Bildgröße auf 64x64 Pixel
        transforms.ToTensor(),  # Konvertiere das Bild in einen Tensor
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        # Normalisiere den Tensor auf den Bereich [-1, 1]
    ])

    # Wende die Transformationen auf das Bild an
    normalized_image = transform(image)

    # Füge eine zusätzliche Dimension hinzu, um die Batch-Dimension (1) zu simulieren
    normalized_image = normalized_image.unsqueeze(0)
    return normalized_image

def calculate_psnr(original_image_path, generated_image_path):
    img_original = cv2.imread(original_image_path)
    img_generated = cv2.imread(generated_image_path)

    psnr_value = cv2.PSNR(img_original, img_generated)
    return round(psnr_value, round_to)

def psnr_to_db(psnr):
    return 10 * math.log10(psnr)

def calculate_lpips(original_image_path, generated_image_path):
    img_original = convert_normalize(original_image_path)
    img_generated = convert_normalize(generated_image_path)

    lpips = LearnedPerceptualImagePatchSimilarity(net_type='vgg')
    score = lpips(img_original, img_generated)

    return round(float(score), round_to)

def calculate_ssim(original_image_path, generated_image_path):
    img_original = cv2.imread(original_image_path)
    img_generated = cv2.imread(generated_image_path)

    # Images_Gray
    img_original_gray = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
    img_generated_gray = cv2.cvtColor(img_generated, cv2.COLOR_BGR2GRAY)

    # Compute SSIM between two images
    (score, diff) = structural_similarity(img_original_gray, img_generated_gray, full=True)

    # diff is in range [0, 1]. Convert it in range [0, 255]
    diff = (diff * 255).astype("uint8")
    #cv2.imshow("Difference", diff)

    # Apply threshold
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # Find contours
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Loop over each contour
    smalest_details = 5

    for contour in contours:
        if cv2.contourArea(contour) > smalest_details:
            # Calculate bounding box
            x, y, w, h = cv2.boundingRect(contour)
            # Draw rectangle bounding box
            cv2.rectangle(img_original, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.rectangle(img_generated, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2.putText(img_generated, "Similarity: " + str(score), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    x = np.zeros(img_original.shape, dtype='uint8')
    result = np.hstack((img_original, x, img_generated))
    # cv2.imshow("Differences", result)
    # cv2.waitKey(0)

    # * 100 for % if needed
    return round(score, round_to)

def calculate_sharpness(original_image_path, generated_image_path):
    img_original = cv2.imread(original_image_path)
    img_generated = cv2.imread(generated_image_path)
    iqa = DOM()

    # Berechnung der Schärfe
    score_original = iqa.get_sharpness(img_original)
    score_generated = iqa.get_sharpness(img_generated)
    # * 100 for %
    return round((score_generated - score_original) * 100, round_to)

def hamming_distance(original_image_path, generated_image_path):
    img_original = Image.open(original_image_path)
    img_generated = Image.open(generated_image_path)

    ahash_original = imagehash.average_hash(img_original)
    ahash_generated = imagehash.average_hash(img_generated)

    hamming_distance = distance.hamming(str(ahash_original), str(ahash_generated))
    return hamming_distance


def create_plot_Reference(models, bildpfade, data):

    diagramm_ueberschrift = data['image_name']

    ueberschriften = ['Original 4x']
    ueberschriften.extend(models)

    texte = [
         f'\n'
         f'\n'
         f'\n'
    #     f'HamDistance: 0\n'
         f'\n'
         f'\n'
    ]
    for model in models:
        methods = [
            f'PSNR: {data[f"psnr_{model}"]}\n'
            f'SSIM: {data[f"ssim_{model}"]}\n'
            f'LPIPS: {data[f"lpips_{model}"]}\n'
            # f'HamDistance: {data[f"ham_distance_{model}"]}\n'
            f'\n'
            f'Sharpness: {data[f"sharpness_{model}"]} %'
        ]
        texte.extend(methods)
     #   print(texte)




    #print('Create PLT')

    # Anzahl der Bilder
    n = len(bildpfade)

    # Größe eines einzelnen Bildes
    bild = mpimg.imread(bildpfade[0])
    bildhoehe, bildbreite, _ = bild.shape

    # Höhe der Textboxen basierend auf der Anzahl der Zeilen im Text
    zeilen_pro_text = max(text.count('\n') + 1 for text in texte)
    textbox_hoehe = zeilen_pro_text * 0.04  # Annahme einer Höhe von 0.04 für jede Zeile

    # Größe des Diagramms basierend auf der Bildhöhe, Textboxhöhe und Anzahl der Bilder
    fig_breite = n * (bildbreite / 100)  # 100 Pixel pro Einheit, zusätzliche 2 Einheiten für die Achsenbeschriftung
    fig_hoehe = (bildhoehe / 100) + 2  # zusätzliche textbox_hoehe Einheiten für die Textboxen und 2 Einheiten für die Achsenbeschriftung

    # Größe des Diagramms
    fig, axs = plt.subplots(1, n, figsize=(fig_breite, fig_hoehe))

    # Schleife zum Hinzufügen der Bilder, Textboxen und Bildüberschriften
    for i in range(n):
        # Bild einlesen
        bild = mpimg.imread(bildpfade[i])
        #print(bildpfade[i])

        # Subplot erstellen und Bild anzeigen
        axs[i].imshow(bild)

        # Achsenticks und -beschriftungen entfernen
        axs[i].set_xticks([])
        axs[i].set_yticks([])

        # Small Images: 12 - 8 - 25
        # Large Images:

        # Textbox für Bildüberschrift erstellen und positionieren
        axs[i].text(0.5, 1.03, ueberschriften[i], fontsize='6', fontweight='bold', transform=axs[i].transAxes,
                    ha='center', va='center')

        # Textbox für Text unter dem Bild erstellen und positionieren
        axs[i].text(0.5, -0.02, texte[i], fontsize='8', transform=axs[i].transAxes, ha='center', va='top')

    # Diagramm-Überschrift hinzufügen
    plt.suptitle(diagramm_ueberschrift, fontsize='15', fontweight='bold')

    # Diagramm anzeigen
    # plt.show()

    # Abstand zwischen den Subplots einstellen
    plt.subplots_adjust(wspace=0.1)

    return fig

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# No Reference IQA Metrics

def calculate_BRISQUE(generated_image_path):
    img_generated = cv2.imread(generated_image_path)

    score = brisque.brisque(img_generated)
    return round(score, round_to)

def calculate_NIQE(generated_image_path):
    img_generated = cv2.imread(generated_image_path)

    score = niqe.niqe(img_generated)
    return round(score, round_to)

def calculate_PIQE(generated_image_path):
    img_generated = cv2.imread(generated_image_path)

    score = piqe.piqe(img_generated)
    return round(score, round_to)

"""
def calculate_MetaIQA(generated_image_path):
    img_generated = cv2.imread(generated_image_path)

    score = MetaIQA.(img_generated)
    return round(score, round_to)
"""

def create_plot_No_Reference(models, bildpfade, data):

    diagramm_ueberschrift = data['image_name']

    #models = ['Original']
    #models.extend(models_in)

    ueberschriften = []
    ueberschriften.extend(models)


    texte = []
    #    f'BRISQUE: -\n'
    #    f'Sharpness: 100 %'
    #]
    for model in models:
        methods = [
            f'BRISQUE: {data[f"brisque_{model}"]}\n'
            f'NIQE: {data[f"niqe_{model}"]}\n'
            f'PIQE: {data[f"piqe_{model}"]}\n'
            f'\n'
            f'Sharpness: {data[f"sharpness_{model}"]} %'
        ]
        texte.extend(methods)
     #   print(texte)

    #print('Create PLT')

    # Anzahl der Bilder
    n = len(bildpfade)

    # Größe eines einzelnen Bildes
    bild = mpimg.imread(bildpfade[0])
    bildhoehe, bildbreite, _ = bild.shape

    # Höhe der Textboxen basierend auf der Anzahl der Zeilen im Text
    zeilen_pro_text = max(text.count('\n') + 1 for text in texte)
    textbox_hoehe = zeilen_pro_text * 0.04  # Annahme einer Höhe von 0.04 für jede Zeile

    # Größe des Diagramms basierend auf der Bildhöhe, Textboxhöhe und Anzahl der Bilder
    fig_breite = n * (bildbreite / 100)  # 100 Pixel pro Einheit, zusätzliche 2 Einheiten für die Achsenbeschriftung
    fig_hoehe = (bildhoehe / 100) + 2  # zusätzliche textbox_hoehe Einheiten für die Textboxen und 2 Einheiten für die Achsenbeschriftung

    # Größe des Diagramms
    fig, axs = plt.subplots(1, n, figsize=(fig_breite, fig_hoehe))

    # Schleife zum Hinzufügen der Bilder, Textboxen und Bildüberschriften
    for i in range(n):
        # Bild einlesen
        bild = mpimg.imread(bildpfade[i])
        #print(bildpfade[i])

        # Subplot erstellen und Bild anzeigen
        axs[i].imshow(bild)

        # Achsenticks und -beschriftungen entfernen
        axs[i].set_xticks([])
        axs[i].set_yticks([])

        # Textbox für Bildüberschrift erstellen und positionieren
        axs[i].text(0.5, 1.03, ueberschriften[i], fontsize='30', fontweight='bold', transform=axs[i].transAxes,
                    ha='center', va='center')

        # Textbox für Text unter dem Bild erstellen und positionieren
        axs[i].text(0.5, -0.02, texte[i], fontsize='25', transform=axs[i].transAxes, ha='center', va='top')

    # Diagramm-Überschrift hinzufügen
    plt.suptitle(diagramm_ueberschrift, fontsize='55', fontweight='bold')

    # Diagramm anzeigen
    # plt.show()

    # Abstand zwischen den Subplots einstellen
    plt.subplots_adjust(wspace=0.1)

    return fig


"""
def find_similar_images(ahash_original, ahash_generated):
    hamming_distance = distance.hamming(str(ahash_original), str(ahash_generated))
    return hamming_distance
"""




"""

# Pandas Dataframe to store the results
df = pd.DataFrame() #columns=['image_name','ahash','phash','dhash','whash','colorhash'])

pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

# initialize Variable for Sharpness evaluation
iqa = DOM()

# Ordnerpfade
folder_path = "../02_ImagesUpscale/"

# Schleife über alle Dateien im Ordner
for file_name in os.listdir(folder_path):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        # Prüfen, ob das Bild das Originalbild ist
        if "_upscaled" in file_name:
            # Generiertes Bild
            generated_image_path = os.path.join(folder_path, file_name)

            # Originalbildpfad erstellen
            original_file_name = file_name.replace("_upscaled", "")
            original_image_path = os.path.join(folder_path, original_file_name)

            # Images
            img_original = cv2.imread(original_image_path)
            img_generated = cv2.imread(generated_image_path)



            # Berechnung von PSNR und SSIM
            psnr_value = calculate_psnr(img_original, img_generated)
            ssim_value = calculate_ssim(img_original, img_generated)

            # Berechnung und vergleich der sharpness zum Original Image
            sharpness = calculate_sharpness(img_original, img_generated)

            # Image Hashing
            # Calculating the average hash (ahash)
            ahash_original, ahash_generated = calculate_hash(original_image_path, generated_image_path)

            # calculateing the Hamming distance for similarities
            hamming_distance = find_similar_images(ahash_original, ahash_generated)

            data = {
                'image_name': original_file_name,
                'psnr_value': psnr_value,
                'ssim_value': ssim_value,
                'sharpness': sharpness,
                'ahash_original': ahash_original,
                'ahash_generated': ahash_generated,
                'hamming_distance': hamming_distance
            }


            #print("original:  " + str(ahash_original))
            #print("generated: " + str(ahash_generated))
            #print("hamming_distance: " + str(hamming_distance))

            # df = df.append(data, ignore_index=True)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)



            # print("Bildpaar:", original_file_name)
            # print("PSNR:", psnr_value)

            # Umrechnung in dB
            #psnr_db = psnr_to_db(psnr_value)
            #print("PSNR (dB):", psnr_db)

            # SSIM
            # print("SSIM:", ssim_value)

            # trashhold = 0.1

            # if sharpness > trashhold:
            #     print("Gennerated Image is sharper: ", sharpness)
            # elif sharpness < -trashhold:
            #     print("Original Image is sharper: ", sharpness)
            # else:
            #     print("Same Shaprness: ", sharpness)


            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

print(df.head(10))
"""