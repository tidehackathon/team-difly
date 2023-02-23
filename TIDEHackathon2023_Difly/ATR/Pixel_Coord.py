import pandas as pd
import os
import warnings

warnings.filterwarnings('ignore')

label_folder = "ATR/Output_alredy_detected/labels" #INSERT HERE THE FOLDER WITH THE YOLO LABELS
csv_folder = "Pixel_coord_Output/csv/"		   #FOLDER WITH ALL THE FRAME, IN .CSV FILES, WITH THE TARGETS FIND IN IT (BOUNDS)	
output_folder = "Pixel_coord_Output/"              #INSERT HERE THE OUTPUT FOLDER

for filename in os.listdir(label_folder):
    if filename.endswith(".txt"):
        pcd = pd.read_csv(os.path.join(label_folder, filename), delimiter=' ', names=['class', 'x_center', 'y_center', 'width', 'height'])
        pcd[['class', 'x_center', 'y_center', 'width', 'height']].to_csv(os.path.join(csv_folder, filename.split('.')[0]+'.csv'), index=None, sep=' ')

for filename in os.listdir(csv_folder):
    if filename.endswith(".csv"):
        pcd = pd.read_csv(os.path.join(csv_folder, filename), delimiter=' ')
        pcd['filename'] = 'a'
        for i in range(0,pcd.shape[0]):
            pcd['x_center'][i] = int(pcd['x_center'][i] * 2757)
            pcd['y_center'][i] = int(pcd['y_center'][i] * 1726)
            pcd['width'][i] = int(pcd['width'][i] * 2757)
            pcd['height'][i] = int(pcd['height'][i] * 1726)
            pcd['filename'][i] = filename
        pcd[['x_center', 'y_center', 'class', 'filename']].to_csv(os.path.join(csv_folder, filename), index=None, sep=' ')
pcd_final = pd.DataFrame()
for filename in os.listdir(csv_folder):
    pcd_new = pd.read_csv(os.path.join(csv_folder, filename), delimiter=' ')
    pcd_final = pcd_final.append(pcd_new)
pcd_final[['x_center', 'y_center', 'class', 'filename']].to_csv(os.path.join(output_folder, 'Pixel_Coord.csv'), index=None, sep=' ')
