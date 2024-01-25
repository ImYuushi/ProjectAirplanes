from torchvision import transforms

from Code import config


def simple_transform():
    transforms = transforms.Compose([
	transforms.ToPILImage(),
	transforms.ToTensor(),
	transforms.Normalize(mean=config.MEAN, std=config.STD)
    ])
    return transforms




def transforms(transform_type : str):
    if (transform_type.equals('simple')):
        return simple_transform()