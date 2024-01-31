from pathlib import Path 
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(Path(__file__).parent.joinpath('Utility')))
sys.path.append(str(path_root))

from Code import config

from Code.Training.Utility import utils
from Code.Training.Utility.engine import train_one_epoch, evaluate
from Code import config
from Code.Training import datasets,transforms
from Code.Training.Models.util import get_model
import torch 
device = 'cpu'
if torch.cuda.is_available() and config.ALLOW_CUDA:
    device = 'cuda'
def validation_split():
    length = np.load(config.data_path.joinpath('Labels').joinpath('labeled_images.npy')).shape[0]





def main():
    transform = transforms.get_transform(train= True)
    train_set, val_set, test_set =  datasets.get_dataset(transform)
    model = get_model()
    model.to(device)


    #create dataloaders 
    data_loader_train = torch.utils.data.DataLoader(
        train_set,
        batch_size=2,
        shuffle=True,
        num_workers=4,
        collate_fn=utils.collate_fn,
        prefetch_factor=4
    )

    
    data_loader_val = torch.utils.data.DataLoader(
        torch.utils.data.ConcatDataset([train_set,val_set]),
        batch_size=1,
        shuffle=False,
        num_workers=4,
        collate_fn=utils.collate_fn
    )
    # construct an optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(
    params,
    lr=0.005,
    momentum=0.5,
    weight_decay=0.0005
    )

    # and a learning rate scheduler
    lr_scheduler = torch.optim.lr_scheduler.StepLR(
        optimizer,
        step_size=3,
        gamma=0.1
    )

    model_path = config.data_path.joinpath('Model_States').joinpath(f'{config.MODELNAME}_{config.VERSION}')
            
    if not (model_path.is_dir()):
        model_path.mkdir()

    if config.START_EPOCH > 0:
        if not (model_path.joinpath(f'epoch_{config.START_EPOCH}.sd').is_file()):
            raise Exception(f'No File for current Version ({config.VERSION}) and epoch ({config.START_EPOCH})')
        else:
            checkpoint = torch.load(str(model_path.joinpath(f'epoch_{config.START_EPOCH}.sd')))
            model.load_state_dict(checkpoint['model_state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            assert(checkpoint['epoch'] == config.START_EPOCH)
    num_epochs = 20
    for epoch in range(config.START_EPOCH,num_epochs):
        # train for one epoch, printing every 10 iterations
        m = train_one_epoch(model, optimizer, data_loader_train, device, epoch, print_freq=100)
        lr_scheduler.step()

        ee = evaluate(model,data_loader_val, device=device)

        st = ''
        for iou,ce in ee.coco_eval.items():
            st+=str(ce.stats)
        model_desc_fp = model_path.joinpath('model_results.txt')
        if not model_desc_fp.is_file():
            model_desc_fp.touch()
        with open(model_desc_fp, 'a')as f:
            f.write(f'===== EPOCH {epoch}=====\n')
            f.write(f'{str(m)}\n')
            f.write(st+'\n') #shhhhhh
            
        torch.save({
                    'model_state_dict':model.state_dict(),
                    'optimizer_state_dict': optimizer.state_dict(),
                    'epoch': epoch
                    }, model_path.joinpath(f'epoch_{epoch}.sd'))





main() 