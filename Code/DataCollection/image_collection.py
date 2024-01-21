
import requests
from pathlib import Path
import re
from datetime import date, timedelta
from tqdm import tqdm
import pandas as pd
import threading
import sys
# path_root = Path(__file__).parents[3]
# sys.path.append(str(path_root))
# print(sys.path)
from Code import config
#cpy from https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
def gen_urls(year,camera):
    link_save_path = config.data_path.joinpath('Websites').joinpath("Image_Links").joinpath(f"img_urls_{camera}_{year}.txt")
    if not link_save_path.is_file():
        link_save_path.touch()
    start_date = date(year, 1, 1)
    end_date = date(year+ 1, 1, 1)
    data_base_url = "https://soho.nascom.nasa.gov/data/REPROCESSING/Completed/"
    print("")
    with open(link_save_path, 'w') as f:
        for single_date in tqdm(daterange(start_date, end_date)):
            s = single_date.strftime("%Y%m%d")
            data_specific_url = data_base_url + f'{year}/{camera}/{s}/'
            rq_html = requests.get(data_specific_url)
            pure_html = rq_html.content
            regex = r'"([A-Za-z0-9]+(_[A-Za-z0-9]+)+)1024\.jpg"'
            lll = re.findall(r'"([A-Za-z0-9]+(_[A-Za-z0-9]+)+)_1024\.jpg"',str(pure_html))
            # print(lll)
            for i in lll:
                picture_specific_url = data_specific_url + i[0] + "_1024.jpg\n"
                f.write(picture_specific_url)

def dl_img(img_save_path_base,line):

    spec_img_path = img_save_path_base.joinpath(line[-26:].rstrip())
    # print(line[-26:].rstrip())
    # print(spec_img_path)
    if not spec_img_path.is_file():
        with open(spec_img_path,'wb') as f2:
            # print(f'downloading: {line[-26:-1]}')
            date = line[-26:-18]
            t = line[-17:-13]
            r = requests.get(line.rstrip(),stream=True)
            for chunk in r.iter_content():
                f2.write(chunk)

        
def download_imgs(year,camera):
    link_save_path = config.data_path.joinpath('Websites').joinpath("Image_Links").joinpath(f"img_urls_{camera}_{year}.txt")
    img_save_path_base = config.data_path.joinpath("images_dl").joinpath(f"images_{year}_{camera}")
    img_save_path_base.mkdir(parents=True, exist_ok=True)
    with open(link_save_path,'r') as f:
        lines = f.readlines()

        n = 1
        for line in tqdm(lines):
            dl_img(img_save_path_base,line)
        # for i in tqdm(range(0,len(lines),n)):
        #     lll = lines[(i*n):((i+1)*n)]
        #     threads = []

        #     for line in lll:
        #         download_thread = threading.Thread(target=dl_img, args=(img_save_path_base,line))
        #         download_thread.start()
        #         threads.append(download_thread)
        #     for t in threads:
        #         t.join()
        #         # print(f'{t} joined')




def create_img_csv(year, camera):
    csv_save_path = config.data_path.joinpath('csvs').joinpath("Image_csvs").joinpath(f"image_data_{year}_{camera}.csv")
    link_save_path = config.data_path.joinpath('Websites').joinpath("Image_Links").joinpath(f"img_urls_{camera}_{year}.txt")

    cols = []
    with open(link_save_path,'r') as f:
        lines = f.readlines()
        for line in lines:
            date = line[-26:-18]
            t = line[-17:-13]
            cols.append({"Date":date,"Time":t})
            # print(date)
            # print(t)
    df = pd.DataFrame.from_dict(cols)
    df.to_csv(csv_save_path)
    print(df)
y = 2020
c = 'c3'
def image_collection(years,cameras, generate = False, create_new_csv = False, download = False):
    for year in years:
        for camera in cameras:
            print(f"Processing {year}/{camera}")
            if generate:
                print("Generating URLS")
                gen_urls(year,camera)
            if create_new_csv:
                print("Creating new IMG csv")
                create_img_csv(year,camera)
            if download:
                download_imgs(year,camera)
# gen_urls(y,c)
# create_img_csv(y,c)
# download_imgs(y, c)
