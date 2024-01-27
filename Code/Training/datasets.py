import os
import torch
from pathlib import Path 
from torchvision.io import read_image
from torchvision.datapoints import BoundingBox
from torchvision import tv_tensors
from torchvision.transforms.v2 import functional as F

from Code import config 

class fixedSizeBBoxesDatasetNoBGLABELS(torch.utils.data.Dataset):
    def __init__(self, root, transform):
        '''
        root should be the base path for all images (i. e. ProjectAirplanes/Data/images_dl/images_2020_c3 at the point of writing this code)
        '''
        self.root = root 
        self.transforms = transforms 
        #format cols: date, time, tel, confirmations, [(coordX,coordY)] for max confs 
        self.imgs = np.load(config.data_path.joinpath('Labels').joinpath('labeled_images.npy'))

    def __getitem__(self,idx):
        date = str(self.imgs[idx,0])
        time = str(self.imgs[idx,1])
        tel = 'c' + str(self.imgs[idx,2])
        while len(time) < 4:
            time = '0' + time 
        img_path = self.root.joinpath(f'{date}_{time}_{tel}_1024.jpg')
        

        img = read_image(img_path)
        img_id = idx 

        #Extract the coordinates of the bounding boxes from self.imgs
        confirmations  = self.imgs[idx,3]
        labels = torch.ones(confirmations, dtype=torch.int64)
        coords = []
        for i in range(confirmations):
            coords+= [(img_with_coords[idx,4+2*i],img_with_coords[idx,5+2*i])]
        data_xCoords = []
        data_yCoords = []
        for i in coords:
                data_xCoords += self.imgs[idx,4+2*i]
                data_yCoords += self.imgs[idx,5+2*i]
  
        boxes = torch.tensor([data_xCoords, data_yCoords])
        img = tv_tensors.Image(img)

        target = {}
        target["boxes"] = tv_tensors.BoundingBoxes(boxes, format="CXCYXY", canvas_size=F.get_size(img))
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd
        
        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    
    def __len__(self):
        return len(self.imgs)