from pathlib import Path 

#global
SEED = 42


ALLOW_CUDA = True
#paths
root_path = Path(__file__).parents[1]
data_path = root_path.joinpath('Data')


#arguments
years = [2020]
cameras = ['c3']

#arguments DataCollection

DC_GENERATE_URLS = False  
DC_CREATE_NEW_CSV = True
DC_DOWNLOAD_IMG = True
DC_CLEANUP = True
IMG_MINSIZE = 741 #in kb

#arguments DataLoading
DL_REDO_VALIDATION_SPLIT = False
DL_RATIO_TRAIN_VAL = 0.2 # should be between 0 and 1 with the value beeing the percentage of the whole dataset being in the validation set

#transforms
IMAGES_MEAN = [0.0091, 0.3035, 0.7609]
IMAGES_STD = [0.0375, 0.0588, 0.0459]
#model
MODELNAME = 'FCNN_RN50'
PRETRAINED = True 
TRAINABLE_BBL = 2

#dataset
USE_ONLY_CONFIRMED  = True
BBOX_H = 20
BBOX_W = 20
TRAIN_SET_LENGTH    = 70 /100
VAL_SET_LENGTH      = 15 / 100
TEST_SET_LENGTH     = 15 / 100


#
VERSION = '1_2(BB20x20)'
START_EPOCH = 0