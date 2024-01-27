from Code import config



def fcnn_resnet50_v1():
    from torchvision.models.detection import fastercnn_resnet50_fpn
    weights = 
    model = fastercnn_resnet50_fpn(weights="DEFAULT", numclasses = 2,trainable_backbone_layers = config.TRAINABLE_BL)
    if not config.PRETRAINED:
        model = fastercnn_resnet50_fpn(numclasses = 2, trainable_backbone_layers = config.TRAINABLE_BBL)
    
    return model

def get_model():

    if (config.MODELNAME == 'FCNN_RN50'):
        return fcnn_resnet50_v1()
    