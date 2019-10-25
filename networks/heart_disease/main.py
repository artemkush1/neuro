import numpy as np
from numpy import genfromtxt
import os
from sys import exit
import keras
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.metrics import Precision, Recall, AUC
from keras.callbacks import ModelCheckpoint, TerminateOnNaN, ReduceLROnPlateau
from keras import backend as K


def f1(y_true, y_pred):
    def recall(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        return recall

    def precision(y_true, y_pred):
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        return precision
    precision = precision(y_true, y_pred)
    recall = recall(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


epochs = 1000
batch_size = 1024


def load_data():
    global tr, trl, te, tel
    data = genfromtxt('heart.csv', delimiter=',')[1:]
    print(data.shape)
    np.random.shuffle(data)
    a = int(len(data) * 0.75)
    tr = data[:a]
    te = data[a:]
    del data
    np.random.shuffle(tr)
    np.random.shuffle(te)
    trl = tr[:, 13]
    tr = tr[:, 0:13]
    tel = te[:, 13]
    te = te[:, 0:13]


def model():
    seq = Sequential()
    seq.add(Dense(13, input_dim=13, activation='relu'))
    seq.add(Dense(1, activation='sigmoid'))
    return seq


def train(seq):
    global history
    seq.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    # checkpoint = ModelCheckpoint('weights.hdf5',
    #                             monitor='val_acc',
    #                             verbose=1,
    #                             save_best_only=True)
    history = seq.fit(tr[:], trl[:], batch_size=batch_size,
                      epochs=epochs, verbose=1,
                      callbacks=[TerminateOnNaN(),
                                 ReduceLROnPlateau(monitor='val_loss',
                                                   factor=0.4,
                                                   patience=50)],
                      validation_data=(te[:], tel[:]),
                      shuffle=True)

    # seq.load_weights(f'weights.hdf5')
    seq.save(f'model')
    print(seq.evaluate(te, tel))


def ploting():
    # print(history.history.keys())
    ac = []
    for i in history.history.keys():
        ac.append(i)
    loss = history.history[ac[2]]
    val_loss = history.history[ac[0]]
    acc = history.history[ac[3]]
    val_acc = history.history[ac[1]]
    epochs = range(1, len(loss) + 1)
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 1, 1)
    ax2 = fig.add_subplot(2, 1, 2)
    ax1.plot(epochs, loss, 'bo', label='Training loss')
    ax1.plot(epochs, val_loss, 'b', label='Validation loss', color='r')
    ax1.set_title('Training and validation loss')
    ax1.set_xlabel('Epochs')
    ax1.set_ylabel('Loss')
    ax1.legend()
    ax2.plot(epochs, acc, 'bo', label='Training acc')
    ax2.plot(epochs, val_acc, 'b', label='Validation acc', color='r')
    ax2.set_title('Training and validation accuracy')
    ax2.set_xlabel('Epochs')
    ax2.set_ylabel('Accuracy')
    ax2.legend()
    for ax in fig.axes:
        ax.grid(True)
    plt.savefig('graph')
    plt.show()


def main():
    load_data()
    m = model()
    train(m)
    ploting()


main()
