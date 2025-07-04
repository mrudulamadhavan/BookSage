from surprise import SVD, NMF, Dataset, Reader
from surprise.model_selection import cross_validate

def train_svd(ratings):
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(ratings[['User-ID', 'ISBN', 'Book-Rating']], reader)
    svd = SVD()
    cross_validate(svd, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    return svd

def train_nmf(ratings):
    reader = Reader(rating_scale=(0, 1))
    data = Dataset.load_from_df(ratings[['User-ID', 'ISBN', 'Book-Rating']], reader)
    nmf = NMF()
    cross_validate(nmf, data, measures=['RMSE', 'MAE'], cv=3, verbose=True)
    return nmf
