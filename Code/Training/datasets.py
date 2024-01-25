import os
import torch
from pathlib import Path 
from torchvision.io import read_image
from torchvision.ops.boxes import masks_to_boxes
from torchvision import tv_tensors
from torchvision.transforms.v2 import functional as F

from Code import config 

class fixedSizeBBoxesDataset(torch.utils.data.Dataset):
    def __init__(self, root, transform):
        '''
        root should be the base path for all images (i. e. ProjectAirplanes/Data/images_dl/images_2020_c3 at the point of writing this code)
        '''
        self.root = root 
        self.transforms = transforms 
        self.imgs = np.load(config.data_path.joinpath('Labels').joinpath('labeled_images.npy'))