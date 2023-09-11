import os
import csv

def convert_txt_to_csv(txt_path, csv_path):
    with open(txt_path, 'r') as txt_file:
        lines = txt_file.readlines()

    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['frame', 'ID', 'x_top_left', 'y_top_left', 'width', 'height', 'type', 'div1', 'div2', 'div3'])

        for line in lines:
            line = line.strip().split(',')
            frame = int(line[0])
            ID = int(line[1])
            x_top_left = float(line[2])
            y_top_left = float(line[3])
            width = float(line[4])
            height = float(line[5])
            type = int(line[6])
            div1 = int(line[7])
            div2 = int(line[8])
            div3 = int(line[9])

            writer.writerow([frame, ID, x_top_left, y_top_left, width, height, type, div1, div2, div3])

def convert_folder_txt_to_csv(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            txt_path = os.path.join(folder_path, filename)
            csv_path = os.path.join(folder_path, os.path.splitext(filename)[0] + '.csv')
            convert_txt_to_csv(txt_path, csv_path)

# Beispielaufruf
folder_path = '00_Original_Videos'
convert_folder_txt_to_csv(folder_path)
