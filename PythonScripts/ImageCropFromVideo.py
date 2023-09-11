import cv2
import os

def extract_bounding_boxes(video_path, txt_path, output_dir):
    # Überprüfe, ob das Video erfolgreich geöffnet werden kann
    video = cv2.VideoCapture(video_path)
    if not video.isOpened():
        print("Fehler beim Öffnen des Videos.")
        return
    # Das Video wurde erfolgreich geladen
    print("Video wurde erfolgreich geladen.")

    # Lese die BoundingBoxen aus der Textdatei
    with open(txt_path, 'r') as file:
        lines = file.readlines()

    # Erstelle das Ausgabeverzeichnis, wenn es noch nicht existiert
    os.makedirs(output_dir, exist_ok=True)

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

        # Extrahiere den Bildbereich (BoundingBox)
        x1 = int(x)
        y1 = int(y)
        x2 = int(x + width)
        y2 = int(y + height)
        bbox = frame[y1:y2, x1:x2]

        # Erstelle den Unterordner für die BoundingBox-ID, falls er nicht existiert
        bbox_dir = os.path.join(output_dir, f'bbox_{bbox_id}')
        os.makedirs(bbox_dir, exist_ok=True)

        # Speichere die BoundingBox als Bild im entsprechenden Unterordner
        output_path = os.path.join(bbox_dir, f'frame_{frame_num}.png')
        cv2.imwrite(output_path, bbox)

        # Berechne und zeige den Fortschritt
        progress = (idx + 1) / len(lines) * 100
        print(f"Fortschritt: {progress:.2f}%")

    # Schließe das Video
    video.release()



# Beispielaufruf
videos_dir = 'original_videos'
output_parent_dir = 'images'

# Liste alle Dateien im Verzeichnis auf
file_names = os.listdir(videos_dir)

# Iteriere über alle Dateien
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

    # Extrahiere BoundingBoxen und speichere sie in Unterordnern
    extract_bounding_boxes(video_path, txt_path, output_dir)


