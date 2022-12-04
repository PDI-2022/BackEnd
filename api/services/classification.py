from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.inception_resnet_v2 import InceptionResNetV2
from tensorflow.keras.models import Model
from api.constants.image import height, width
from api.services.storage import create_folder
from keras.layers import Dropout
import tensorflow as tf
import numpy as np
import pandas as pd

test_data_dir = "./images/imagens_cortadas/"

batch_size = 1

def model():
    base_model = InceptionResNetV2(include_top=False, weights="imagenet")
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='sigmoid')(x)
    x = Dense(128, activation='relu')(x)
    x = Dense(32, activation='relu')(x)
    x = Dropout(0.2)(x)
    predictions = Dense(7, activation='softmax')(x)
    model = Model(inputs=base_model.input, outputs=predictions)

def classificate(model ,model_path : str, classes):

        create_folder(test_data_dir)

        test_datagen = ImageDataGenerator(rescale=1./255)

        test_generator = test_datagen.flow_from_directory(
                test_data_dir,
                target_size=(height, width),
                shuffle=False,
                batch_size=batch_size)

        image_list = []      
        files = test_generator.filenames
        for img_path in files:
                label = img_path.split("-")
                print(label)
                label = label[-1].split(".jpg")
                dados = int(label[0])
                image_list.append(dados)

        labels = {0: "classe_1",
                1: "classe_2",
                2: "classe_3",
                3: "classe_4",
                4: "classe_5",
                5: "classe_6",
                6: "classe_7"}

        model = tf.keras.models.load_model(model_path)

        predictions = model.predict(test_generator)

        y_pred = (np.floor((np.argmax(predictions, axis=1) * classes/7)) + 1)


        list_csv = []
        for i in range(len(y_pred)):
                csv = [image_list[i], y_pred[i]]
                list_csv.append(csv)

        df = pd.DataFrame(list_csv, columns=['SEMENTE', 'CLASSE'])
        df = df.sort_values(by=['SEMENTE'])
        predicao = df['CLASSE'].to_numpy()
        print(predicao)

        return predicao
