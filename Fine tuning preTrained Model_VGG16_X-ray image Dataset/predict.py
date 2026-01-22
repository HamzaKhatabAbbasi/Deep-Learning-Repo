# deep_learning_pipeline/predict.py

from sklearn.metrics import accuracy_score, classification_report

def make_predictions(model, X_test, y_test):
    probs = model.predict(X_test)
    preds = (probs > 0.5).astype(int)

    print("\nClassification Report:\n", classification_report(y_test, preds))
    print("Accuracy:", accuracy_score(y_test, preds))

    index = 4
    specific_prob = model.predict(X_test[index].reshape(1, 224, 224, 3))
    specific_pred = (specific_prob > 0.5).astype(int)
    print(f"\nSample Prediction at index {index}:", specific_pred[0][0])
    print("Actual Label:", y_test[index])
