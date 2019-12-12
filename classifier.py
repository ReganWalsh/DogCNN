import ast
from PIL import Image
import torchvision.transforms as transforms
from torch.autograd import Variable
import torchvision.models as models
from torch import __version__

resnet18 = models.resnet18(pretrained=True)
alexnet = models.alexnet(pretrained=True)
vgg16 = models.vgg16(pretrained=True)

models = {'resnet': resnet18, 'alexnet': alexnet, 'vgg': vgg16}

#Get ImageNet labels
with open('imagenet1000_clsid_to_human.txt') as imagenet_classes_file:
    imagenet_classes_dict = ast.literal_eval(imagenet_classes_file.read())

def classifier(img_path, model_name):
    #Load The Image
    img_pil = Image.open(img_path)

    #Transform For Consistency
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    img_tensor = preprocess(img_pil)
    img_tensor.unsqueeze_(0)
    
    pytorch_ver = __version__.split('.')
    if int(pytorch_ver[0]) > 0 or int(pytorch_ver[1]) >= 4:
        img_tensor.requires_grad_(False)
    else:
        #Apply Model To Input And Wrap Input In Variable
        data = Variable(img_tensor, volatile = True) 

    #Apply Model To Input
    model = models[model_name]

    #Puts Model In Evaluation Mode
    model = model.eval()
    
    #Apply Data To Model
    if int(pytorch_ver[0]) > 0 or int(pytorch_ver[1]) >= 4:
        output = model(img_tensor)
    else:
        output = model(data)

    #Return Index Corresponding To Predicted Class
    pred_idx = output.data.numpy().argmax()

    return imagenet_classes_dict[pred_idx]
