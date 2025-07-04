from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np

def evaluate_rmse(true_ratings, predicted_ratings):
    return np.sqrt(mean_squared_error(true_ratings, predicted_ratings))

def evaluate_mae(true_ratings, predicted_ratings):
    return mean_absolute_error(true_ratings, predicted_ratings)

def precision_at_k(predicted, actual, k=5):
    relevant = set(actual)
    recommended = set(predicted[:k])
    return len(recommended & relevant) / float(k)
