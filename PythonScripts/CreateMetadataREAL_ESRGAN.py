import os

def write_file_names(root_folder, output_file):
    with open(output_file, 'w') as f:
        for foldername, subfolders, filenames in os.walk(root_folder):
            for filename in filenames:
                relative_path = os.path.relpath(foldername, root_folder)
                file_path = os.path.join(relative_path, filename)
                f.write(file_path + '\n')

# Beispielaufruf:
root_folder = '../Upscaler/Real_ESRGAN/datasets/finetune_small'  # Gib hier den Pfad zu deinem Root-Ordner an
output_file = '../Upscaler/Real_ESRGAN/datasets/finetune_small/meta_info_finetune.txt'  # Gib hier den gewünschten Dateinamen für die Ausgabedatei an

write_file_names(root_folder, output_file)
