import os
import torch
from pathlib import Path 
from torchvision.io import read_image
# from torchvision.datapoints import BoundingBox
# import torchivsion.datapoints.BoundingBox
from torchvision import tv_tensors
from torchvision.transforms.v2 import functional as F
from torch.utils.data import random_split
import numpy as np
from Code import config 

class fixedSizeBBoxesDatasetNoBGLABELS(torch.utils.data.Dataset):
    def __init__(self, root, transforms):
        '''
        root should be the base path for all images (i. e. ProjectAirplanes/Data/images_dl/images_2020_c3 at the point of writing this code)
        '''
        self.root = root 
        self.transforms = transforms 
        #format cols: date, time, tel, confirmations, [(coordX,coordY)] for max confs 
        self.imgs = np.load(config.data_path.joinpath('Labels').joinpath('labeled_images.npy'))
        if config.USE_ONLY_CONFIRMED:
            self.imgs = np.load(config.data_path.joinpath('Labels').joinpath('confirmation_images.npy'))
        # self.indices = indices 

    def __getitem__(self,idx):
        # idx = self.indices[index]
        date = str(self.imgs[idx,0])
        time = str(self.imgs[idx,1])
        tel = 'c' + str(self.imgs[idx,2])
        while len(time) < 4:
            time = '0' + time 
        img_path = self.root.joinpath(f'{date}_{time}_{tel}_1024.jpg')
        

        img = read_image(str(img_path))
        image_id = idx 

        #Extract the coordinates of the bounding boxes from self.imgs
        confirmations  = self.imgs[idx,3]
        labels = torch.ones(confirmations, dtype=torch.int64)
        data_xCoords = []
        data_yCoords = []

        for i in range(confirmations):
            data_xCoords += [self.imgs[idx,4+2*i]]
            y = -(self.imgs[idx,5+2*i] - 1023)
            # if not (y >= 0 and y <=1023):
            #     print (f'y BL idx = {self.imgs[idx,5+2*i]}\ny new idx = {y}')
            data_yCoords += [y]
        boxes = torch.empty([confirmations,4], dtype=torch.int16)
        
        for i in range(confirmations):
            cX = data_xCoords[i]
            cY = data_yCoords[i]
            x0 = max(cX - (config.BBOX_W/2),0)
            x1 = min(cX + (config.BBOX_W/2),1024)
            y0 = max(cY - (config.BBOX_H/2),0)
            y1 = min(cY + (config.BBOX_H/2),1024)
            boxes[i,0] = x0 
            boxes[i,1] = y0
            boxes[i,2] = x1 
            boxes[i,3] = y1
            # areas[i] = (x1 - x0 ) * (y1 - y0)
        areas = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # areas = torch.tensor(areas)
        # boxes = torch.tensor(boxes)
        # img = tv_tensors.Image(img)
        # bboxes = []
        # for i in range(confirmations):
        #     xCoord = 
        iscrowd = torch.zeros((confirmations,), dtype=torch.int64)
        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = areas
        target["iscrowd"] = iscrowd
        
        if self.transforms is not None:
            img, target = self.transforms(img, target)
            # img = self.transforms(img)

        return img, target
        # return img, 0
        # if self.transforms is not None:        
        #     sample = self.transforms(image = img,
        #                             bboxes = target['boxes'],
        #                             labels = labels)
        #     img = sample['image']
        #     target['boxes'] = torch.Tensor(sample['bboxes'])

        # return img_res, target
        
    def __len__(self):
        return len(self.imgs)


def get_dataset(transform):
    dataset = fixedSizeBBoxesDatasetNoBGLABELS(root = config.data_path.joinpath('Images'), transforms=transform)
    indices = torch.randperm(len(dataset),generator=torch.Generator().manual_seed(config.SEED)).tolist()
    perc = [config.TRAIN_SET_LENGTH, config.VAL_SET_LENGTH, config.TEST_SET_LENGTH]
    n = len(indices)
    a = int(n*config.TRAIN_SET_LENGTH)
    b = int(n*config.VAL_SET_LENGTH)
    c = int(n*config.TEST_SET_LENGTH)
    indices_train   = indices[:a]
    indices_val     = indices[a:a+b]
    indices_test    = indices[a+b:a+b+c]
    print(f'trainlength: {len(indices_train)}')
    train_set = torch.utils.data.Subset(dataset,indices_train)
    val_set =  torch.utils.data.Subset(dataset,indices_val)
    test_set =  torch.utils.data.Subset(dataset,indices_test)
    # dataset_test = torch.utils.data.Subset(dataset_test, indices[-50:])
    # 

    # train_set, val_set, test_set = random_split(ds,lengths=[config.TRAIN_SET_LENGTH, config.VAL_SET_LENGTH, config.TEST_SET_LENGTH]\
    #   ,generator=torch.Generator().manual_seed(config.SEED))


    return train_set, val_set, test_set