# deep_learning_pipeline/models/vgg16_model.py

from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

def build_model():
    base_model = VGG16(weights='imagenet', include_top=True, input_shape=(224, 224, 3))

    model = Sequential()
    for layer in base_model.layers[:-1]:
        model.add(layer)

    for layer in model.layers:
        layer.trainable = False

    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model
