import os
import pandas as pd
import Comparison as comparison
import matplotlib.pyplot as plt


# Pandas Dataframe to store the results
df = pd.DataFrame()

pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)




# models = ['Photoshop', 'ESRGAN', 'REAL_ESRGAN', 'BSRGAN', 'SwinIR', 'StableDiffusion']
models = ['REAL_ESRGAN', 'REAL_ESRGAN-FIN']

# Ordnerpfade
#ä folder_path = "../04_Biggest_50/01_OnLowRes/01_Compare"
# folder_original_img = '00_Original'

folder_path = "Finetune"
folder_original_img = 'Original'

# output_path = '00_LowResComparison/samples'
output_path = 'Finetune/Ergebnis'


total_files = 0
completed_files = 0
for root, dirs, files in os.walk(folder_path + '/' + folder_original_img):
    total_files += len(files)

# Schleife über alle Dateien im Ordner
for file_name in os.listdir(folder_path + '/' + folder_original_img):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        img_original_path = folder_path + '/' + folder_original_img + '/' + file_name
        data_ges = {}
        bildpfade = [img_original_path]

        for model in models:
            img_gen_path = folder_path + '/' + model + '/' + file_name

            psnr = comparison.calculate_psnr(img_original_path, img_gen_path)
            ssim = comparison.calculate_ssim(img_original_path, img_gen_path)
            lpips = comparison.calculate_lpips(img_original_path, img_gen_path)
            sharpness = comparison.calculate_sharpness(img_original_path, img_gen_path)
            # ham_distance = comparison.hamming_distance(img_original_path, img_gen_path)

            data = {
                f'image_name': file_name,
                f'psnr_{model}': psnr,
                f'ssim_{model}': ssim,
                f'lpips_{model}': lpips,
                f'sharpness_{model}': sharpness
                # f'ham_distance_{model}': ham_distance
            }

            # update data liste mit allen Modelldaten
            data_ges.update(data)
            #print(data_ges)

            bildpfade.append(img_gen_path)
            #print(bildpfade)


        # Create Plot
        plt_result = comparison.create_plot_Reference(models, bildpfade, data_ges)

        # Diagramm anzeigen
        #plt_result.show()
        plt_result.savefig(output_path + '/' + data_ges['image_name'])

        # füge alle modelldaten zu dem df hinzu
        df = pd.concat([df, pd.DataFrame([data_ges])], ignore_index=True)


        # Fortschritsanzeigen in %
        completed_files += 1
        percent_completed = (completed_files / total_files) * 100
        print(f'Progress: {percent_completed:.2f}%')



#print('\n')
#print(df)