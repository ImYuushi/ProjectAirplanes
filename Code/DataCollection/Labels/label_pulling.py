import requests as rq 
import pathlib
import re
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
    open(html_path,'wb').write(r.content)

def download_comets(year):
    data = open(html_paths(year)).read()
    matches_path = re.findall(r"/sites/sungrazer/files/comet_txts/soho\d+_xy\.txt", data)
    matches_comets = re.findall(r"soho\d+_xy\.txt", data)
    matches = list(map(lambda x, y:(x,y), matches_path, matches_comets)) 
    print(matches)
    # assert(len(matches_comets) == len(matches_path))
    for comet_url_path, comet_name in matches:
        url = 'https://sungrazer.nrl.navy.mil' + comet_url_path
        r = rq.get(url, allow_redirects=False)
        comet_save_path = comet_path().joinpath(comet_name)
        if not comet_save_path.is_file():
            comet_save_path.touch()
        print('Creating file for' + comet_name)
        open(comet_save_path,'wb').write(r.content)


        

    


def create_labels_csv(years):
    for i in years:
        download_yearly_htmls(i)
        comet_urls = download_comets(i)


# create_labels_csv([2018,2019,2020,2021])
create_labels_csv([2021])
