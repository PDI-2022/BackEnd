import os
import cv2
from .embriao_model import *


def deteccao(embriao_folder, embriao_model, img, index):

    embriao_res = embriao_detect(embriao_model, img)

    for ret, _, _ in embriao_res:
        if (ret[3] - ret[1]) / (ret[2] - ret[0]) > 0.5:

            embriao_cortado = img[ret[1] : ret[3], ret[0] : ret[2]]
            if len(embriao_cortado) > 0:
                cv2.imwrite(
                    "{0}/semente-{1}.jpg".format(embriao_folder, str(index + 1)),
                    embriao_cortado,
                )
