from pathlib import Path 

import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
# print(str(path_root))
# print(sys.path)
from Code import config
from Code.DataCollection.image_collection import image_collection
from Code.DataCollection.label_pulling import collect_labels

# root_path = path_root
# print(config.root_path)

#This File must not be moved from ProjectAirplanes/Code/DataCollection, else relative imports go boo



# print('Collecting Labels')
collect_labels()
print('Collecting Images')
image_collection(config.years, config.cameras,generate = False, create_new_csv=True, download=False)
# image_collection(config.years, config.cameras,generate = False, create_new_csv=False, download=True)
