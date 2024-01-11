import requests as rq 
import pathlib
import re
from tqdm import tqdm
import pandas as pd 
#Inputs: years (list)
#Result: For each comet discovered that year, every found occurence will be added to a csv, with all the relevant data(TODO)


"""
for each year
    step 1: download html containing links for comet discoveries
    step 2: parse the links
    step 3: download all txt files witht he comet data
    step 4: parse the text files into csvs 
"""
def html_paths(year):
    return (pathlib.Path(__file__).parent).joinpath('Websites').joinpath('comet_tables').joinpath(f'comet_table_{year}.html')
def url_path(year):
    return "https://sungrazer.nrl.navy.mil/comets_table_"+ str(year)
def comet_path():
     return (pathlib.Path(__file__).parent).joinpath('Websites').joinpath('comet_data')


def download_yearly_htmls(year):
    html_path = html_paths(year)
    url_complete = url_path(year)
    r = rq.get(url_complete, allow_redirects=True)
    if not html_path.is_file():
        html_path.touch()
    print(f'Creating file for html for year {year}\n ')
    with open(html_path,'wb') as f:
        f.write(r.content)

def download_comets(year):
    data = open(html_paths(year)).read()
    matches_path = re.findall(r"/sites/sungrazer/files/comet_txts/soho\d+_xy\.txt", data)
    matches_comets = re.findall(r"soho\d+_xy\.txt", data)
    matches = list(map(lambda x, y:(x,y), matches_path, matches_comets)) 
    # print(matches)
    # assert(len(matches_comets) == len(matches_path))
    for comet_url_path, comet_name in tqdm(matches, leave=False):
        url = 'https://sungrazer.nrl.navy.mil' + comet_url_path
        r = rq.get(url, allow_redirects=False)
        comet_save_path = comet_path().joinpath(comet_name)
        if not comet_save_path.is_file():
            comet_save_path.touch()
        # print('Creating file for' + comet_name)
        with open(comet_save_path,'wb') as f:
            f.write(r.content)

def parse_single_commet(comet_str):
    comet_lines = str(comet_str).splitlines()
    assert(comet_lines[4] == "#    DATE     TIME    TEL    COL     ROW  ")
    comet_name = comet_lines[0][1:]
    cnt = 0
    l = []
    for line in comet_lines[5:]:
        sighting = line.split(" ")
        sighting = list(filter(lambda x: x is not '', sighting))
        try:
            l.append({"Name" : comet_name, "Date": sighting[0], "Time": sighting[1], "Tel" : sighting[2], "Col" : sighting[3], "Row" : sighting[4]})
        except:
            cnt = 1
            # print(comet_name)
            # print(sighting)
            # print(line)
    if cnt:
        print("Problem with " + comet_name)
    return l
    



def parse_all_comets():
    l = list(comet_path().glob("*"))
    comet_data_list = []
    for r in l:
        with open(r) as file:
            s  = file.read()
            comet_data_list+= (parse_single_commet(s))

    # print(comet_data_list)
    df = pd.DataFrame.from_dict(comet_data_list)
    df.to_csv("all_comets.csv")
    # print(comet_data_list[0])
    print(df)

    


def create_labels_csv(years):
    for i in years:
        download_yearly_htmls(i)
        comet_urls = download_comets(i)
def clean_dead_urls():
    l = list(comet_path().glob("*"))
    total = 0
    dead = 0
    for r in l:
        total+= 1
        s  = open(r).read()
        if not s.startswith("#"):
            pathlib.Path.unlink(r)
            # print(r)
            dead+= 1
    print(f'cleaned {dead} / {total}')
        


# create_labels_csv([2018,2019,2020,2021])
# create_labels_csv([2021])
# create_labels_csv(range(1996,2022))
# clean_dead_urls()
parse_all_comets()

