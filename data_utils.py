import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def load_data():
    books = pd.read_csv('data/BX-Books.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
    ratings = pd.read_csv('data/BX-Book-Ratings-Subset.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
    users = pd.read_csv('data/BX-Users.csv', sep=';', encoding='latin-1', on_bad_lines='skip')
    return books, ratings, users

def preprocess_ratings(ratings):
    ratings = ratings[ratings['Book-Rating'] > 0]
    ratings['Book-Rating'] = MinMaxScaler().fit_transform(ratings[['Book-Rating']])
    return ratings
