import tensorflow as tf
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Dropout, Conv2D
from keras.callbacks import TensorBoard
from src.neural.dataLoader.loadKaggleV3 import trainingGenerator, testGenerator
from sklearn.model_selection import train_test_split
# à utiliser avec la base de donnée kaggleV3 (src.neural.dataBuilder.buildKaggleV3)

def buildModel():
    # the tensorboard callBack 
    nbChunksTraining = 370
    nbChunksTest = 8

    testGene = testGenerator(nbChunksTest)
    trainingGene = trainingGenerator(nbChunksTraining)
    tbCallBack = TensorBoard(log_dir='./Graph', histogram_freq=0, write_graph=True, write_images=True)

    model = Sequential([
        Conv2D(filters=128,kernel_size=[3,3],activation="relu", input_shape=(28, 28, 1)),
        Conv2D(filters=64,kernel_size=[3,3],activation="relu"),
        Flatten(),
        Dense(128, activation='sigmoid'),
        Dense(128, activation='sigmoid'),
        Dropout(0.5),
        Dense(26, activation='softmax'),
    ])

    model.compile(optimizer="adam",
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"])

    model.fit_generator(trainingGene, epochs=4, steps_per_epoch=nbChunksTraining, validation_data=testGene, callbacks=[tbCallBack], 
                        use_multiprocessing=True, workers=4)

    return model

def saveModel(model):
    model.save("src/neural/RNN/model/hand_written_recognition_Conv.model")

