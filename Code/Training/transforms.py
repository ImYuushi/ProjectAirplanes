# from torchvision import transforms

# from Code import config


# def simple_transform():
#     transforms = transforms.Compose([
# 	transforms.ToPILImage(),
# 	transforms.ToTensor(),
# 	transforms.Normalize(mean=config.MEAN, std=config.STD)
#     ])
#     return transforms




# def transforms(transform_type : str):
#     if (transform_type.equals('simple')):
#         return simple_transform()
from torchvision.transforms import v2 as T


def get_transform(train):
    transforms = []
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    transforms.append(T.ToDtype(torch.float, scale=True))
    transforms.append(T.ToPureTensor())
    return T.Compose(transforms)