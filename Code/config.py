from pathlib import Path 



root_path = Path(__file__).parents[1]
print('aa')
print(root_path)


data_path = root_path.joinpath('Data')

years = [2020]
cameras = ['c3']