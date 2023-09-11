import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import cv2
import Comparison as comparison

filename = 'achau-02_left_23_4.png'

path = '../04_Biggest_50/01_OnLowRes'
#path = '../04_Biggest_50/02_OnOriginal'

bild_01_original = f'{path}/01_Original/{filename}'
bild_02_photoshop = f'{path}/Photoshop/{filename}'
bild_03_RealESRGAN = f'{path}/03_REAL_ESRGAN/{filename}'
bild_04_Upscayl = f'{path}/04_Upscayl/{filename}'
bild_05_TopazGigapixel = f'{path}/05_TopazGigapixel/{filename}'
bild_06_SwinIR = f'{path}/06_SwinIR/{filename}'



# ----------------------------------------------------------------------------------------------------------------------

# Liste der Bildpfade
bildpfade = [
    bild_01_original,
    bild_02_photoshop,
    bild_03_RealESRGAN,
    bild_04_Upscayl,
    bild_05_TopazGigapixel,
    bild_06_SwinIR
]

# Liste der Texte für jede Textbox
texte = [
    f'PSNR: -\n'
    f'SIM: 100 %\n'
    f'HamDistance: 0\n'
    f'\n'
    f'Sharpness: 100 %',

    f'PSNR: {psnr_origninal_photoshop}\n'
    f'SIM: {ssim_original_phototshop} %\n'
    f'HamDistance: {hamming_distance_original_Photoshop}\n'
    f'\n'
    f'Sharpness: {sharpness_original_Photoshop} %',

    f'PSNR: {psnr_origninal_RealESRGAN}\n'
    f'SIM: {ssim_original_RealESRGAN} %\n'
    f'HamDistance: {hamming_distance_original_RealESRGAN}\n'
    f'\n'
    f'Sharpness: {sharpness_original_RealESRGAN} %',

    f'PSNR: {psnr_origninal_Upscayl}\n'
    f'SIM: {ssim_original_Upscayl} %\n'
    f'HamDistance: {hamming_distance_original_Upscayl}\n'
    f'\n'
    f'Sharpness: {sharpness_original_Upscayl} %',

    f'PSNR: {psnr_origninal_TopazGigapixel}\n'
    f'SIM: {ssim_original_TopazGigapixel} %\n'
    f'HamDistance: {hamming_distance_original_TopazGigapixel}\n'
    f'\n'
    f'Sharpness: {sharpness_original_TopazGigapixel} %',

    f'PSNR: {psnr_origninal_SwinIR}\n'
    f'SIM: {ssim_original_SwinIR} %\n'
    f'HamDistance: {hamming_distance_original_SwinIR}\n'
    f'\n'
    f'Sharpness: {sharpness_original_SwinIR} %'
]

# Liste der Bildüberschriften
ueberschriften = [
    'Original 4x',
    'Photoshop',
    'Real_ESRGAN',
    'Upscayl',
    'TopazGigapixel',
    'SwinIR'
]

# Überschrift des Diagramms
diagramm_ueberschrift = 'achau-02_left_23_4 -- Frame: 220'

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

    # Subplot erstellen und Bild anzeigen
    axs[i].imshow(bild)

    # Achsenticks und -beschriftungen entfernen
    axs[i].set_xticks([])
    axs[i].set_yticks([])

    # Textbox für Bildüberschrift erstellen und positionieren
    axs[i].text(0.5, 1.03, ueberschriften[i], fontsize='large', fontweight='bold', transform=axs[i].transAxes, ha='center', va='center')

    # Textbox für Text unter dem Bild erstellen und positionieren
    axs[i].text(0.5, -0.02, texte[i], fontsize='large', transform=axs[i].transAxes, ha='center', va='top')

# Diagramm-Überschrift hinzufügen
plt.suptitle(diagramm_ueberschrift, fontsize='x-large', fontweight='bold')

# Abstand zwischen den Subplots einstellen
plt.subplots_adjust(wspace=0.1)

# Diagramm anzeigen
plt.show()