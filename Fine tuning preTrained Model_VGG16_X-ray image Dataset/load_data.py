# deep_learning_pipeline/data/load_data.py

import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

base_dir = 'x-ray_dataset'
img_size = (224, 224)

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=20,
    zoom_range=0.2,
    horizontal_flip=True
)

test_val_datagen = ImageDataGenerator(rescale=1./255)

def extract_batches(generator):
    X, y = [], []
    for _ in range(len(generator)):
        images, labels = next(generator)
        X.append(images)
        y.append(labels)
    return np.concatenate(X), np.concatenate(y)

def load_data():
    train_gen = train_datagen.flow_from_directory(
        os.path.join(base_dir, 'train'),
        target_size=img_size,
        class_mode='binary'
    )

    val_gen = test_val_datagen.flow_from_directory(
        os.path.join(base_dir, 'val'),
        target_size=img_size,
        class_mode='binary'
    )

    test_gen = test_val_datagen.flow_from_directory(
        os.path.join(base_dir, 'test'),
        target_size=img_size,
        class_mode='binary',
        shuffle=False
    )

    X_train, y_train = extract_batches(train_gen)
    X_val, y_val = extract_batches(val_gen)
    X_test, y_test = extract_batches(test_gen)

    return X_train, y_train, X_val, y_val, X_test, y_test
