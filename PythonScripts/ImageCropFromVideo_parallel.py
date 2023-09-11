import cv2
import os
from multiprocessing import Pool, cpu_count
import threading


def process_video(video_path, txt_path, output_dir):
    # Überprüfe, ob das Video erfolgreich geöffnet werden kann
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print(f"Fehler beim Öffnen des Videos: {video_path}")
        return

    # Das Video wurde erfolgreich geladen
    print(f"Video wurde erfolgreich geladen: {video_path}")

    # Lese die BoundingBoxen aus der Textdatei
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    # Erstelle das Ausgabeverzeichnis, wenn es noch nicht existiert
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.splitext(os.path.basename(video_path))[0]

    # Verarbeite jede Zeile in der Textdatei
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    for idx, line in enumerate(lines):
        line = line.strip().split(',')
        frame_num = int(line[0])
        bbox_id = int(line[1])
        x = float(line[2])
        y = float(line[3])
        width = float(line[4])
        height = float(line[5])

        # Springe zum gewünschten Frame im Video
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_num - 1)  # Frames beginnen bei 0, daher Abzug von 1

        # Lies das Frame
        ret, frame = video.read()

        # Überprüfe den Rückgabewert von video.read()
        if not ret:
            print(f"Fehler beim Lesen des Frames {frame_num}.")
            continue

        image_height, image_width, _ = frame.shape

        # Extrahiere den Bildbereich (BoundingBox) und passe negative Koordinaten an
        x1 = int(max(0, x))
        y1 = int(max(0, y))
        x2 = int(x + width)
        y2 = int(y + height)

        # Überprüfe und korrigiere die Koordinaten, um sicherzustellen, dass sie innerhalb des Bildes liegen
        x1 = min(x1, image_width)
        y1 = min(y1, image_height)
        x2 = min(x2, image_width)
        y2 = min(y2, image_height)

        # Berechne die tatsächliche Breite und Höhe der BoundingBox nach Anpassung der Koordinaten
        adjusted_width = x2 - x1
        adjusted_height = y2 - y1

        # Extrahiere den Bildbereich (BoundingBox) basierend auf den angepassten Koordinaten
        bbox = frame[y1:y2, x1:x2]

        # Erstelle den Unterordner für die BoundingBox-ID, falls er nicht existiert
        bbox_dir = os.path.join(output_dir, f'bbox_{bbox_id}')
        os.makedirs(bbox_dir, exist_ok=True)

        # Speichere die BoundingBox als Bild im entsprechenden Unterordner
        output_path = os.path.join(bbox_dir, f'{filename}_{bbox_id}_{frame_num}.png')

        lock.acquire()
        try:
            cv2.imwrite(output_path, bbox)
        finally:
            # Entsperre den Lock
            lock.release()

        # Berechne und zeige den Fortschritt
        progress = (idx + 1) / len(lines) * 100
        print(f"Video: {filename}, Fortschritt: {progress:.2f}%")

    # Schließe das Video
    video.release()


def process_video_wrapper(args):
    return process_video(*args)

# Erstelle ein Lock-Objekt
lock = threading.Lock()

if __name__ == '__main__':
    # Beispielaufruf
    # videos_dir = '00_Original_Videos'
    output_parent_dir = '01_Original_Images'

    # Liste alle Dateien im Verzeichnis auf
    file_names = os.listdir(videos_dir)

    # Erstelle eine Liste der Argumente für jeden Video-Verarbeitungsprozess
    process_args = []
    for file_name in file_names:
        # Überprüfe, ob die Datei eine .mp4-Datei ist
        if not file_name.endswith('.mp4'):
            continue

        # Pfade für das aktuelle Video und die dazugehörige Textdatei
        video_path = os.path.join(videos_dir, file_name)
        txt_file_name = os.path.splitext(file_name)[0] + '.txt'
        txt_path = os.path.join(videos_dir, txt_file_name)

        # Überprüfe, ob die Textdatei vorhanden ist
        if not os.path.isfile(txt_path):
            print(f"Keine Textdatei gefunden für: {file_name}")
            continue

        # Erstelle einen separaten Ausgabeordner für das aktuelle Video
        video_name = os.path.splitext(file_name)[0]
        output_dir = os.path.join(output_parent_dir, video_name)
        os.makedirs(output_dir, exist_ok=True)

        # Füge die Argumente zur Prozessliste hinzu
        process_args.append((video_path, txt_path, output_dir))

    # Verarbeite die Videos parallel mit Hilfe von multiprocessing
    with Pool(processes=cpu_count()) as pool:
        pool.map(process_video_wrapper, process_args)

    print("Verarbeitung abgeschlossen.")
