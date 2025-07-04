import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def content_based_recommendations(books_df, book_title, top_n=5):
    tfidf = TfidfVectorizer(stop_words='english')
    books_df['Book-Title'] = books_df['Book-Title'].fillna('')
    tfidf_matrix = tfidf.fit_transform(books_df['Book-Title'])

    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(books_df.index, index=books_df['Book-Title']).drop_duplicates()

    idx = indices.get(book_title)
    if idx is None:
        return pd.DataFrame()

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]

    book_indices = [i[0] for i in sim_scores]
    return books_df.iloc[book_indices]
