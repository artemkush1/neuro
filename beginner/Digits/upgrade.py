from keras import models
from keras import layers
from keras import losses
from keras import optimizers
from keras.datasets import mnist
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt


# <============PLOTING============>#


def ploting():
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    acc = history.history['acc']
    val_acc = history.history['val_acc']
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
    plt.show()


# <============DATASET============>#


(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
train_images = train_images.reshape((60000, 28, 28, 1))
train_images = train_images.astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1))
test_images = test_images.astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


# <============CREATE MODEL============>#


model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu',
                        input_shape=(28, 28, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(10, activation='softmax'))

print(model.summary())


# <============COMPILE MODEL============>#


'''
# test_acc: 0.9914000034332275
model.compile(optimizer='rmsprop',
              loss='mse',
              metrics=['acc'],
              loss_weights=None,
              sample_weight_mode=None,
              weighted_metrics=None,
              target_tensors=None)
'''

# test_acc: 0.9886999726295471
model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['acc'],
              loss_weights=None,
              sample_weight_mode=None,
              weighted_metrics=None,
              target_tensors=None)


''' <============SAME_RESULT============>
model.compile(optimizer=optimizers.RMSprop(lr=0.001),
              loss='mse',
              metrics=['acc'])
'''


# <============TRAINING============>#


history = model.fit(x=train_images,
                    y=train_labels,
                    batch_size=128,
                    epochs=5,
                    verbose=1,
                    callbacks=None,
                    validation_split=0.0,
                    validation_data=(test_images, test_labels),
                    shuffle=True,
                    class_weight=None,
                    sample_weight=None,
                    initial_epoch=0,
                    steps_per_epoch=None,
                    validation_steps=None,
                    validation_freq=1,
                    max_queue_size=10,
                    workers=1,
                    use_multiprocessing=False)


# <============RESULT FOR TEST DATA============>#


test_loss, test_acc = model.evaluate(x=test_images,
                                     y=test_labels,
                                     batch_size=None,
                                     verbose=1,
                                     sample_weight=None,
                                     steps=None,
                                     callbacks=None,
                                     max_queue_size=10,
                                     workers=1,
                                     use_multiprocessing=False)


'''  Prediction'''

print((model.predict(train_images[0:1, :, :, :])))


# <============PRINT============>#


print(f'test_acc: {test_acc}\ntest_loss: {test_loss}')
ploting()


