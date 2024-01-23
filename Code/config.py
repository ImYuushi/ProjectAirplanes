from pathlib import Path 

#global
SEED = 42



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

