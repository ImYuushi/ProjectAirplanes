from pathlib import Path
import numpy as np 
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
from torchvision import transforms
import math



from Code import config

#return ImageFolders which contain
# for {Validation Set, Train Set}w




def dataloading_ready():
    """
    Returns True if both Images/Validation_set/* and Images/Training_set/* contain files with the proportion (DL_RATIO_VAL_TRAIN)
    """
   
    image_dir = config.data_path.joinpath('Images')
    image_conf_dir = image_dir.joinpath('Conf')
    image_noconf_dir= image_dir.joinpath('NoConf')
    
    val_set_dir = image_dir.joinpath('Validation_set')
    train_set_dir = image_dir.joinpath('Training_set')


    files_train_set = [f for f in train_set_dir.rglob('*') if f.is_file()]
    files_val_set = [f for f in val_set_dir.rglob('*') if f.is_file()]

    #TODO: This is not complete, this might not catch an incomplete dataset but oh well
    if (len(files_train_set) == 0 or len(files_val_set) == 0\
        or not val_set_dir.is_dir() or not train_set_dir.is_dir()):
        return False
    if ((len(files_train_set) * (0.9 * (1/(1 - DL_RATIO_TRAIN_VAL))) <= len(files_val_set) * (1/DL_RATIO_TRAIN_VAL)) \
    and (len(files_train_set) * (1.1 * (1/(1 - DL_RATIO_TRAIN_VAL))) >= len(files_val_set)* (1/DL_RATIO_TRAIN_VAL))): #if
        return False
    else:
        return True

def dataloading_splitting():

    image_dir = config.data_path.joinpath('Images')
    image_conf_dir = image_dir.joinpath('Conf')
    image_noconf_dir= image_dir.joinpath('NoConf')



    val_set_dir = image_dir.joinpath('Validation_set')
    train_set_dir = image_dir.joinpath('Training_set')
        

    print(val_set_dir)
    print(train_set_dir)
    # return
    files_conf = [f for f in image_conf_dir.iterdir() if f.is_file()]
    files_noconf = [f for f in image_noconf_dir.iterdir() if f.is_file()]
    print(f'len conf ({len(files_conf)}) len noconf ({len(files_noconf)})')
    # return
    if (len(files_conf) == 0 or len(files_noconf) == 0):
        files_train_set = [f for f in train_set_dir.rglob('*') if f.is_file()]
        files_val_set = [f for f in val_set_dir.rglob('*') if f.is_file()]
        if (len(files_train_set) == 0 or len(files_val_set) == 0):
            raise Exception(f'Trying to Seperate Images into Val/Train sets, \
                        but no images in images/conf and Images/NoConf,\
                         nor in Images/Validation_set (size={len(len(files_val_set))})\
                          or Images/Training_set (size={len(files_train_set)})\n \
                          This means there are no images where they should be after running preprocessing.py. If that was done, no images were downloaded')
        else:
            #Move everything back to Images/Conf and Images/NoConf respectively
            image_conf_dir.mkdir()
            image_noconf_dir.mkdir()
            for f in (files_train_set + files_val_set):
                f_name = f.name 
                f_category = f.parent 
                print(f'movving ({f}) to ({config.data_path.joinpath(f_category).joinpath(f_name)})')
                # f.rename(config.data_path.joinpath(f_category).joinpath(f_name))
    if not (val_set_dir.is_dir()):
        val_set_dir.mkdir()
    if not (train_set_dir.is_dir()):
        train_set_dir.mkdir()           
    if not (val_set_dir.joinpath('Conf').is_dir()):
        (val_set_dir.joinpath('Conf')).mkdir()
    if not (train_set_dir.joinpath('Conf').is_dir()):
        (train_set_dir.joinpath('Conf')).mkdir()
    if not (val_set_dir.joinpath('NoConf').is_dir()):
        (val_set_dir.joinpath('NoConf')).mkdir()
    if not (train_set_dir.joinpath('NoConf').is_dir()):
        (train_set_dir.joinpath('NoConf')).mkdir()
    files_all = files_conf + files_noconf
    np.random.seed(config.SEED)
    np.random.shuffle(files_all)

    train_set_length =math.floor(len(files_all) * (1-config.DL_RATIO_TRAIN_VAL))


    train_set_files = files_all[:train_set_length]
    val_set_files = files_all[train_set_length:]
    for f in train_set_files:
        f_name = f.name
        f_category = f.parent.name 
        # print(f'moving ({f}) to ({train_set_dir.joinpath(f_category).joinpath(f_name)})')
        f.rename(train_set_dir.joinpath(f_category).joinpath(f_name))
    for f in val_set_files:
        f_name = f.name
        f_category = f.parent.name
        # print(f'moving ({f}) to ({val_set_dir.joinpath(f_category).joinpath(f_name)})')
        f.rename(val_set_dir.joinpath(f_category).joinpath(f_name))

    

def dataloading():
    if config.DL_REDO_VALIDATION_SPLIT or not dataloading_ready():
        dataloading_splitting()

