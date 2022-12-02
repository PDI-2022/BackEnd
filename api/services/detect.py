import torch
import cv2
from api.services.storage import create_folder
from .embriao_model import *
import os, glob
from api.constants.folders import embriao_folder

def deteccao(embriao_model, img,index):      
    create_folder(embriao_folder)

    embriao_res = embriao_detect(embriao_model, img)

    for ret, _, _ in embriao_res:
            if((ret[3]-ret[1])/(ret[2]-ret[0]) > 0.6):
                
                
                embriao_cortado = img[ret[1]:ret[3], ret[0]:ret[2]]
                if len(embriao_cortado) > 0:
                    cv2.imwrite(f'./images/embrioes/semente-'+ str(index+1) + '.jpg', embriao_cortado)
