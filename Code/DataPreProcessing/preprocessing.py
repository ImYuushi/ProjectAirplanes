import pandas as pd 
from pathlib import Path 
from tqdm import tqdm
import shutil
import sys
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



def main(years,cameras):
    df_labels = pd.read_csv(config.data_path.joinpath("Labels").joinpath("raw_confirmation_data.csv")).drop(['Unnamed: 0'], axis=1)
    df_filtered_labels = pd.DataFrame(columns = df_labels.columns, index = df_labels.index, data=None)
    # df_filtered_labels
    df_img = pd.DataFrame()
    print(df_filtered_labels)
    for year in years:
        for camera in cameras:
            df_tmp = filter_labels(year,camera, df_labels)
            if df_img.empty:
                df_img = pd.read_csv(config.data_path.joinpath("Image_tables").joinpath(f'image_data_{year}_{camera}.csv'),dtype={"Unnamed: 0": int, "Date" : str, "Time" : str})
                df_img = df_img.drop(['Unnamed: 0'], axis=1)
                df_img['Tel'] = camera
                df_filtered_labels = df_tmp
            else:
                df_tmp_img = pd.read_csv(config.ata_path.joinpath("Image_tables").joinpath(f'image_data_{year}_{camera}.csv'))
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
        
    print(df_img.sort_values('Confirmations'))
    poss = df_img[df_img['Confirmations']> 0].shape[0]
    negs = df_img.shape[0] - poss 
    print(f'In {years} with cameras ({cameras}) there are a total of {df_img.shape[0]} comets\n P/N ratio: {poss}/{negs}')
    df_img['Label'] = 0
    df_img.loc[df_img['Confirmations'] > 0, 'Label'] = 1
    print(df_img.sort)
    df_img.to_csv(config.data_path.joinpath('csvs').joinpath("PreProcessed_data.csv"), index=False)



#No need for parameter, since we only work with preprocessed_data.csv, which' creation required the year/camera parameters

def moving_imgs():
    df = pd.read_csv(config.data_path.joinpath('csvs').joinpath('PreProcessed_data.csv'), index=False)
    if not (config.data_path.joinpath('Images').is_dir()):
        Path.mkdir(config.data_path.joinpath('Images'))
    if not (config.data_path.joinpath('Images').joinpath('Conf').is_dir()):
        Path.mkdir(config.data_path.joinpath('Conf').joinpath('Images'))
    if not (config.data_path.joinpath('Images').joinpath('NoConf').is_dir()):
        Path.mkdir(config.data_path.joinpath('NoConf').joinpath('Images'))
    
    
    
    for _,row in tqdm(df.iterrows()):
        row_time = row['Time']
        row_date = row['Date']
        tel = row['Tel']
        t = row_time.replace(":","")[:4]
        d = row_date.replace("-", '')
        image_path = config.data_path.joinpath(f'images_dl')\
                    .joinpath(f'images_{d[:4]}_{tel.lower()}')\
                    .joinpath(f'{d}_{t}_{tel.lower()}_1024.jpg')
        image_path_new = data_path.joinpath('Images')
        if (row['Label'] == 0):
            image_path_new = image_path_new.joinpath('NoConf')
        else:
            iamge_path_new = image_path_new.joinpath('Conf')
        shutil.move(image_path,image_path_new)


# main([2020],["c3"])