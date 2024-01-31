from Code import config



def fcnn_resnet50_v1():
    from torchvision.models.detection import fasterrcnn_resnet50_fpn

    model = fasterrcnn_resnet50_fpn(weights="DEFAULT", numclasses = 2,trainable_backbone_layers = config.TRAINABLE_BBL)
    if not config.PRETRAINED:
        model = fastercnn_resnet50_fpn(numclasses = 2, trainable_backbone_layers = config.TRAINABLE_BBL)
    
    return model

