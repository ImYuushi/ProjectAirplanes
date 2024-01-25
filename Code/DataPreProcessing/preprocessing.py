import pandas as pd 
from pathlib import Path 
from tqdm import tqdm
import shutil
import sys
import numpy as np
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
from Code import config
# base_path = Path(__file__).parent.parent.parent
# data_path = base_path.joinpath("Data")
"""
    We make an assumption about the data, that for any image, a commet appears only once, not twice, altough multiple different comets can be there, which sounds obvious,
    but I use this at some point later in the code

    - At no minute, are there two or more pictures

"""

def filter_labels(year,camera, df_labels):
    df_tmp = df_labels
    df_tmp = df_tmp.loc[df_tmp['Tel'] == camera.upper()]
    
    df_tmp = df_tmp.loc[df_tmp['Date'].str.startswith(str(year))]
    print(df_tmp.sort_values(by='Date',ascending=False))
    print(year)
    return df_tmp



#TODO: data only goes to 2021-01-25... I think



# def adding_labels(years,cameras):
#     df_labels = pd.read_csv(config.data_path.joinpath("csvs").joinpath("raw_confirmation_data.csv")).drop(['Unnamed: 0'], axis=1)
#     df_filtered_labels = pd.DataFrame(columns = df_labels.columns, index = df_labels.index, data=None)
#     # df_filtered_labels
#     df_img = pd.DataFrame()
#     # print(df_filtered_labels)
#     for year in years:
#         for camera in cameras:
#             df_tmp = filter_labels(year,camera, df_labels)
#             if df_img.empty:
#                 df_img = pd.read_csv(config.data_path.joinpath('csvs').joinpath("Image_csvs").joinpath(f'image_data_{year}_{camera}.csv'),dtype={"Unnamed: 0": int, "Date" : str, "Time" : str})
#                 df_img = df_img.drop(['Unnamed: 0'], axis=1)
#                 df_img['Tel'] = camera
#                 df_filtered_labels = df_tmp
#             else:
#                 df_tmp_img = pd.read_csv(config.data_path.joinpath('csvs').joinpath("Image_csvs").joinpath(f'image_data_{year}_{camera}.csv'))
#                 df_tmp_img.drop(['Unnamed: 0'], axis=1, inplace=True)
#                 df_img = pd.concat([df_img,df_tmp_img])
#                 df_img['Tel'] = camera
#                 df_filtered_labels = pd.concat([df_filtered_labels,df_tmp])
#     df_img["Confirmations"] = 0

#     for _, row in tqdm(df_filtered_labels.iterrows()):
#         row_time = row['Time']
#         row_date = row['Date']
#         tel = row['Tel']
#         t = row_time.replace(":","")[:4]
#         d = row_date.replace("-", '')
#         df_img.loc[(df_img['Time'] == t) & (df_img['Date'] == d) & (df_img['Tel'] == tel.lower()),'Confirmations'] += 1
        
        
#     # print(df_img.sort_values('Confirmations'))
#     poss = df_img[df_img['Confirmations']> 0].shape[0]
#     negs = df_img.shape[0] - poss 
#     print(f'In {years} with cameras ({cameras}) there are a total of {df_img.shape[0]} comets\n P/N ratio: {poss}/{negs}')
#     df_img['Label'] = 0
#     df_img.loc[df_img['Confirmations'] > 0, 'Label'] = 1
#     # print(df_img.sort)
#     df_img.to_csv(config.data_path.joinpath('csvs').joinpath("PreProcessed_data.csv"), index=False)

def adding_labels2(years,cameras):
    df_labels = pd.read_csv(config.data_path.joinpath("csvs").joinpath("raw_confirmation_data.csv")).drop(['Unnamed: 0'], axis=1)
    df_filtered_labels = pd.DataFrame(columns = df_labels.columns, index = df_labels.index, data=None)
    # df_filtered_labels
    df_img = pd.DataFrame()
    # print(df_filtered_labels)
    for year in years:
        for camera in cameras:
            df_tmp = filter_labels(year,camera, df_labels)
            if df_img.empty:
                df_img = pd.read_csv(config.data_path.joinpath('csvs').joinpath("Image_csvs").joinpath(f'image_data_{year}_{camera}.csv'),dtype={"Unnamed: 0": int, "Date" : str, "Time" : str})
                df_img = df_img.drop(['Unnamed: 0'], axis=1)
                df_img['Tel'] = camera
                df_filtered_labels = df_tmp
            else:
                df_tmp_img = pd.read_csv(config.data_path.joinpath('csvs').joinpath("Image_csvs").joinpath(f'image_data_{year}_{camera}.csv'))
                df_tmp_img.drop(['Unnamed: 0'], axis=1, inplace=True)
                df_img = pd.concat([df_img,df_tmp_img])
                df_img['Tel'] = camera
                df_filtered_labels = pd.concat([df_filtered_labels,df_tmp])
    df_img["Confirmations"] = 0
    
    for _, row in tqdm(df_filtered_labels.iterrows()):
        row_time = row['Time']
        row_date = row['Date']
        tel = row['Tel']
        t = row_time.replace(":","")[:4]
        d = row_date.replace("-", '')
        df_img.loc[(df_img['Time'] == t) & (df_img['Date'] == d) & (df_img['Tel'] == tel.lower()),'Confirmations'] += 1
    # col_names = [('Time',str), ('Confirmations',str)] + sum([[(f'xCoord{i}',int),(f'yCoord{i}',int)] for i in range(df_img['Confirmations'].max())],[])
    # print(col_names)
    max_confs = df_img['Confirmations'].max()
    # df_img_with_coords = pd.DataFrame(columns=[i[0] for i in col_names] )
    # print(df_img_with_coords.dtypes)
    #logic here is: 3 cols for identifiers (date, time, tel (as number, since we only use c cameras)), 1 col for #confirmations, and 2 cols for each confirmation for x and y coord
    n = 3+ 1 + 2 * max_confs
    img_with_coords = np.zeros((df_img.shape[0], (n)),dtype=np.int32) 

    for idx,row in tqdm(df_img.iterrows()):
        img_with_coords[idx][0] = int(row['Date'])
        img_with_coords[idx][1] = int(row['Time'])
        img_with_coords[idx][2] = int(row['Tel'][1]) # c3 -> 3 as an example
        img_with_coords[idx][3] = row['Confirmations']
    # print(img_with_coords[10,:])
    df_img.to_csv(config.data_path.joinpath("urmom.csv"))
    for _, row in tqdm(df_filtered_labels.iterrows()):
        row_time = row['Time']
        row_date = row['Date']
        tel = row['Tel']
        t = row_time.replace(":","")[:4]
        d = row_date.replace("-", '')
        target_img = df_img.loc[(df_img['Time'] == t) & (df_img['Date'] == d) & (df_img['Tel'] == tel.lower())]
        target_idx = target_img.index 
        if (target_img.shape[0] != 1):
            print(f'd: ({d}), t: ({t}), tel: ({tel})')
            continue
        assert(target_img.shape[0] == 1)
        assert(int(target_img.iloc[0]['Date']) == img_with_coords[target_idx,0])
        start = 4
        while img_with_coords[target_idx,start] != 0:
            start += 2
            if start >= n:
                print(img_with_coords.astype(int)[target_idx])
                raise Exception("This was never supposed to happen")
        
        img_with_coords[target_idx,start] = round(row['Col'])
        img_with_coords[target_idx,start + 1] = round(row['Row'])
        # print(f'row: ({img_with_coords[target_idx,start]}) col: ({img_with_coords[target_idx,start]})')
    np.save(config.data_path.joinpath('Labels').joinpath('labeled_images.npy'),img_with_coords)
    

#No need for parameter, since we only work with preprocessed_data.csv, which' creation required the year/camera parameters

def moving_imgs():
    df = pd.read_csv(config.data_path.joinpath('csvs').joinpath('PreProcessed_data.csv'),\
                    dtype = {'Date' : str, 'Time' : str, 'Tel': str, 'Confirmations' : int, 'Label' : int})
    
    if not (config.data_path.joinpath('Images').is_dir()):
        Path.mkdir(config.data_path.joinpath('Images'))
    if not (config.data_path.joinpath('Images').joinpath('Conf').is_dir()):
        Path.mkdir(config.data_path.joinpath('Images').joinpath('Conf'))
    if not (config.data_path.joinpath('Images').joinpath('NoConf').is_dir()):
        Path.mkdir(config.data_path.joinpath('Images').joinpath('NoConf'))
    
    
    
    for _,row in tqdm(df.iterrows()):
        row_time = row['Time']
        row_date = row['Date']
        tel = row['Tel']
        t = row_time
        d = row_date
        # return
        #this code here is stupid, it could be easier with using .name, oh well
        image_path = config.data_path.joinpath(f'images_dl')\
                    .joinpath(f'images_{d[:4]}_{tel.lower()}')\
                    .joinpath(f'{d}_{t}_{tel.lower()}_1024.jpg')
        image_path_new = config.data_path.joinpath('Images')
        if (row['Label'] == 0):
            image_path_new = image_path_new.joinpath('NoConf')
        else:
            image_path_new = image_path_new.joinpath('Conf')
        # print(f'moving from ({image_path}) to ({image_path_new})')
        shutil.move(image_path,image_path_new)


def preprocessing():
    adding_labels2(config.years, config.cameras)
    # moving_imgs()


preprocessing()