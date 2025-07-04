import streamlit as st
import pandas as pd
from data_utils import load_data, preprocess_ratings
from recommender import content_based_recommendations
import template as t

st.set_page_config(page_title="BookSage 📚", layout="wide")
st.title("📚 BookSage – Your Wise Reading Companion")

books, ratings, users = load_data()
ratings = preprocess_ratings(ratings)

# Session Defaults
if 'User-ID' not in st.session_state:
    st.session_state['User-ID'] = 98783
if 'ISBN' not in st.session_state:
    st.session_state['ISBN'] = '0385486804'

# Sidebar Choice
st.sidebar.header("📖 Start Your Journey")
choice = st.sidebar.radio("How would you like to begin?", ["Select a Favorite Book", "Choose a Genre"])

if choice == "Select a Favorite Book":
    title = st.sidebar.selectbox("Pick your favorite book:", books['Book-Title'].dropna().unique())
    isbn = books[books['Book-Title'] == title]['ISBN'].values[0]
    t.select_book(isbn)
else:
    genres = ["Fiction", "Romance", "Science", "Fantasy", "Mystery", "History", "Biography"]
    selected_genre = st.sidebar.selectbox("Pick a genre:", genres)
    genre_books = books[books['Book-Title'].str.contains(selected_genre, case=False, na=False)]
    if not genre_books.empty:
        sample = genre_books.sample(1).iloc[0]
        t.select_book(sample['ISBN'])

# Display selected book
book = books[books['ISBN'] == st.session_state['ISBN']].iloc[0]
rating_data = ratings[ratings['ISBN'] == st.session_state['ISBN']]
avg_rating = rating_data['Book-Rating'].mean()

cover, info = st.columns([1, 3])
with cover:
    st.image(book['Image-URL-L'], use_column_width=True)
with info:
    st.subheader(book['Book-Title'])
    st.markdown(f"**Author:** {book['Book-Author']}")
    st.markdown(f"**Publisher:** {book['Publisher']} ({book['Year-Of-Publication']})")
    st.markdown(f"**Average Rating:** {avg_rating:.1f} ⭐" if not pd.isna(avg_rating) else "No ratings yet.")

st.caption("“A reader lives a thousand lives before he dies.” – George R.R. Martin")

# Top-rated by User
st.subheader("🎯 Books You Rated Highly")
user_id = st.session_state['User-ID']
user_books = ratings[(ratings['User-ID'] == user_id) & (ratings['Book-Rating'] >= 0.8)]
top_books = books[books['ISBN'].isin(user_books['ISBN'])].drop_duplicates('Book-Title').head(5)
t.recommendations(top_books)
st.caption("“You know you've read a good book when you turn the last page and feel a little as if you have lost a friend.” – Paul Sweeney")

# Cross-genre recs
st.subheader("🌍 Explore New Genres")
genre_list = ["Fiction", "Romance", "Science", "Fantasy", "Mystery", "History", "Biography"]
current_genre = next((g for g in genre_list if g.lower() in book['Book-Title'].lower()), None)

for genre in genre_list:
    if genre == current_genre:
        continue
    genre_df = books[books['Book-Title'].str.contains(genre, case=False, na=False)]
    merged = genre_df.merge(ratings, on='ISBN')
    if not merged.empty:
        top = merged.groupby('ISBN').mean(numeric_only=True).sort_values(by='Book-Rating', ascending=False).head(1)
        if not top.empty:
            isbn_top = top.index[0]
            book_row = books[books['ISBN'] == isbn_top]
            st.markdown(f"**{genre} Pick**")
            t.recommendations(book_row)

st.caption("“Fill your house with stacks of books, in all the crannies and all the nooks.” – Dr. Seuss")

st.markdown("---")
st.caption("📚 Powered by BookCrossing | Your recommendations are uniquely yours 🌟")
