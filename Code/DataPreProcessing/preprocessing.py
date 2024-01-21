import pandas as pd 
from pathlib import Path 
from tqdm import tqdm
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
    df_labels = pd.read_csv(config.data_path.joinpath("Labels").joinpath("all_comet_confirmations.csv")).drop(['Unnamed: 0'], axis=1)
    df_filtered_labels = pd.DataFrame(columns = df_labels.columns, index = df_labels.index, data=None)
    # df_filtered_labels
    df_img = pd.DataFrame()
    print(df_filtered_labels)
    for year in years:
        for camera in cameras:
            df_tmp = filter_labels(year,camera, df_labels)
            if df_img.empty:
                df_img = pd.read_csv(data_path.joinpath("Image_tables").joinpath(f'image_data_{year}_{camera}.csv'),dtype={"Unnamed: 0": int, "Date" : str, "Time" : str})
                df_img = df_img.drop(['Unnamed: 0'], axis=1)
                df_img['Tel'] = camera
                df_filtered_labels = df_tmp
            else:
                df_tmp_img = pd.read_csv(data_path.joinpath("Image_tables").joinpath(f'image_data_{year}_{camera}.csv'))
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
    df_img.to_csv(data_path.joinpath("PreProcessed_data.csv"), index=False)

def collect_labels():
    create_labels_csv(range(1996,2023))
    clean_dead_urls()
    parse_all_comets()

# main([2020],["c3"])