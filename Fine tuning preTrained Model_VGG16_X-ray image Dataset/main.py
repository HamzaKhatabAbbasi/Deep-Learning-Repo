# deep_learning_pipeline/main.py

from load_data import load_data
from vgg16_model import build_model
from train import train_model
from predict import make_predictions

if __name__ == "__main__":
    X_train, y_train, X_val, y_val, X_test, y_test = load_data()
    model = build_model()
    history = train_model(model, X_train, y_train, X_val, y_val, epochs=10)
    make_predictions(model, X_test, y_test)
