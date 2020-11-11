import torch.nn as nn
from torchvision.models.detection.retinanet import RetinaNet, retinanet_resnet50_fpn, RetinaNetHead
from torchvision.models.detection.backbone_utils import resnet_fpn_backbone
from vision.models.components import create_torchvision_backbone

__all__ = ["create_vision_retinanet", "create_retinanet_backbone"]


def create_vision_retinanet(num_classes: int = 91, backbone: nn.Module = None, **kwargs,):
    """
    Creates RetinaNet implementation based on torchvision library.
    Args:
    num_classes (int) : number of classes.
    Do not have class_id "0" it is reserved as background.
    num_classes = number of classes to label + 1 for background.
    """
    if backbone is None:
        model = retinanet_resnet50_fpn(pretrained=True, num_classes=91, **kwargs,)
        model.head = RetinaNetHead(
            in_channels=model.backbone.out_channels,
            num_anchors=model.head.classification_head.num_anchors,
            num_classes=num_classes,)
    else:
        model = RetinaNet(backbone, num_classes=num_classes, **kwargs)

    return model


def create_retinanet_backbone(name: str, fpn: bool = True, pretrained: bool = True,
                              trainable_backbone_layers: int = 3, **kwargs) -> nn.Module:
    """
    Args:
        name (str): If none creates a default resnet50_fpn model trained on MS COCO 2017
            Supported backones are: "resnet18", "resnet34","resnet50", "resnet101", "resnet152",
            "resnext50_32x4d", "resnext101_32x8d", "wide_resnet50_2", "wide_resnet101_2",
            as resnets with fpn backbones.
            Without fpn backbones supported are: "resnet18", "resnet34", "resnet50","resnet101",
            "resnet152", "resnext101_32x8d", "mobilenet", "vgg11", "vgg13", "vgg16", "vgg19",
        fpn (bool): If True then constructs fpn as well.
        pretrained (bool): Creates a pretrained backbone with imagenet weights.
    """
    if fpn:
        # Creates a torchvision resnet model with fpn added.
        backbone = resnet_fpn_backbone(name, pretrained,
                                       trainable_layers=trainable_backbone_layers, **kwargs)
    else:
        # This does not create fpn backbone, it is supported for all models
        backbone, _ = create_torchvision_backbone(name, pretrained)
    return backbone
