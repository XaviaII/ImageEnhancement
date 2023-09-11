import os
from PIL import Image
import shutil
from tqdm import tqdm  # Fortschrittsanzeige-Bibliothek

# Pfad zum Eingabeordner mit den Bildern
eingabe_ordner = "Pfad/zum/Eingabeordner"

# Pfad zum Ausgabeordner für die größten 50 Bilder
ausgabe_ordner = "Pfad/zum/Ausgabeordner"

# Erstelle den Ausgabeordner, falls er noch nicht existiert
if not os.path.exists(ausgabe_ordner):
    os.makedirs(ausgabe_ordner)

# Liste für die Bildgrößen und Pfade der größten 50 Bilder
groesste_bilder = []

# Durchlaufe die Ordnerstruktur und berechne die Bildgröße für jedes Bild
for ordnername, unter_ordner, dateien in os.walk(eingabe_ordner):
    for datei in tqdm(dateien, desc="Verarbeite Bilder"):  # Fortschrittsanzeige
        bild_pfad = os.path.join(ordnername, datei)
        try:
            with Image.open(bild_pfad) as bild:
                # Berechne die Bildgröße
                breite, hoehe = bild.size
                bild_groesse = breite * hoehe

                # Füge das Bild zur Liste der größten Bilder hinzu
                groesste_bilder.append((bild_groesse, bild_pfad))
        except (IOError, OSError):
            # Ignoriere Dateien, die keine Bilder sind
            pass

# Sortiere die Bilder nach ihrer Größe in absteigender Reihenfolge
groesste_bilder.sort(reverse=True)

# Kopiere die größten 50 Bilder in den Ausgabeordner
for bild_groesse, bild_pfad in tqdm(groesste_bilder[:50], desc="Kopiere Bilder"):  # Fortschrittsanzeige
    bild_dateiname = os.path.basename(bild_pfad)
    ziel_pfad = os.path.join(ausgabe_ordner, bild_dateiname)
    shutil.copy2(bild_pfad, ziel_pfad)

print("Die größten 50 Bilder wurden erfolgreich kopiert.")
