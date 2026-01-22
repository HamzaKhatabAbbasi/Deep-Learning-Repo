# deep_learning_pipeline/models/train.py

import os
import matplotlib.pyplot as plt

def train_model(model, X_train, y_train, X_val, y_val, epochs=10):
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=epochs
    )

    plt.figure(figsize=(10, 4))
    plt.plot(history.history['accuracy'], label='Training Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Model Accuracy')
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.show()

    plt.figure(figsize=(10, 4))
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    plt.show()

    # Save the trained model
    os.makedirs('saved_model', exist_ok=True)
    model.save('saved_model/vgg16_xray_model.h5')
    print("✅ Model saved to saved_model/vgg16_xray_model.h5")

    return history
