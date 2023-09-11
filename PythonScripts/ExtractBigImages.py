import os
from PIL import Image
import shutil
from tqdm import tqdm

# Pfad zum Eingabeordner mit den Bildern
eingabe_ordner = "../02_ImagesUpscale/00_GroundTruth_Images"

# Pfad zum Ausgabeordner für die größten Bilder
ausgabe_ordner = "test_03"

# Anzahl bilder pro Unterordner
img_sub_count = 1

# Anzal an bildern die davon ausgewählt werden
img_count = 100

# Erstelle den Ausgabeordner, falls er noch nicht existiert
if not os.path.exists(ausgabe_ordner):
    os.makedirs(ausgabe_ordner)

# Liste für die Bildgrößen und Pfade der größten Bilder
groesste_bilder = []

# Durchlaufe die Ordnerstruktur und berechne die Bildgröße für jedes Bild in den Unterordnern
for ordnername, unter_ordner, dateien in os.walk(eingabe_ordner):
    for unterordner in unter_ordner:
        unterordner_pfad = os.path.join(ordnername, unterordner)
        bilder_in_unterordner = []

        # Durchlaufe die Dateien im aktuellen Unterordner
        for datei in os.listdir(unterordner_pfad):
            bild_pfad = os.path.join(unterordner_pfad, datei)
            try:
                with Image.open(bild_pfad) as bild:
                    # Berechne die Bildgröße
                    breite, hoehe = bild.size
                    bild_groesse = breite * hoehe

                    # Füge das Bild zur Liste der Bilder im Unterordner hinzu
                    bilder_in_unterordner.append((bild_groesse, bild_pfad))
            except (IOError, OSError):
                # Ignoriere Dateien, die keine Bilder sind
                pass

        # Sortiere die Bilder im Unterordner nach ihrer Größe in absteigender Reihenfolge
        bilder_in_unterordner.sort(reverse=True)

        # Füge die größten 10 Bilder des Unterordners zur Gesamtliste hinzu
        groesste_bilder.extend(bilder_in_unterordner[:img_sub_count])

# Sortiere die Gesamtliste nach der Größe in absteigender Reihenfolge
groesste_bilder.sort(reverse=True)

# Kopiere die größten Bilder in den Ausgabeordner
for bild_groesse, bild_pfad in tqdm(groesste_bilder[:img_count], desc="Kopiere Bilder"):
    bild_dateiname = os.path.basename(bild_pfad)
    ziel_pfad = os.path.join(ausgabe_ordner, bild_dateiname)
    shutil.copy2(bild_pfad, ziel_pfad)

print("Die größten 10 Bilder jedes Unterordners wurden erfolgreich kopiert.")
