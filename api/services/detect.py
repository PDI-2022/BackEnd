import cv2
from api.services.storage import create_folder
from .embriao_model import *


def deteccao(embriao_folder, embriao_model, img, index):
    create_folder(embriao_folder)

    embriao_res = embriao_detect(embriao_model, img)

    for ret, _, _ in embriao_res:
        if (ret[3] - ret[1]) / (ret[2] - ret[0]) > 0.6:

            embriao_cortado = img[ret[1] : ret[3], ret[0] : ret[2]]
            if len(embriao_cortado) > 0:
                cv2.imwrite(
                    "{0}/semente-.jpg".format(embriao_cortado, str(index + 1)), img
                )
