from pathlib import Path 
from torch.utils.data import randomsplit()


from Code import config
from Code.Training import datasets,transforms
from Code.Training.Models import get_model

def validation_split():
    length = np.load(config.data_path.joinpath('Labels').joinpath('labeled_images.npy')).shape[0]





def main():
    transform = transforms.get_transform(train= True)
    train_set, val_set, test_set =  get_dataset(transform)
    #make a dataloader for all three sets 

    #do loss function

    #do LR adjustment stuff

    #make a train function incorporating everything
    
    #do eval function 

    #debug
    #debug
    #debug more




