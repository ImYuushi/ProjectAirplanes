from Code.Training.Models.fcnn_resnet50 import fcnn_resnet50_v1
from Code import config
import torchvision
def get_model():

    if (config.MODELNAME == 'FCNN_RN50'):
        return fcnn_resnet50_v1()
    else:
        # load a model pre-trained pre-trained on COCO
        model = torchvision.models.detection.fasterrcnn_resnet50_fpn(weights="DEFAULT", numclasses = 2,trainable_backbone_layers = config.TRAINABLE_BBL)
        from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
        # get number of input features for the classifier
        in_features = model.roi_heads.box_predictor.cls_score.in_features
        # replace the pre-trained head with a new one
        model.roi_heads.box_predictor = FastRCNNPredictor(in_features, 2) 

        return model