import streamlit as st
from random import random

def select_book(isbn):
  st.session_state['ISBN'] = isbn

def select_user(userid):
  st.session_state['User-ID'] = userid

def tile_item(column, item):
  with column:
    st.button('📖', key=random(), on_click=select_book, args=(item['ISBN'], ))
    st.image(item['Image-URL-M'], use_column_width='always')
    st.caption(item['Book-Title'])

def recommendations(df):
  if df.shape[0] == 0:
    st.info("No recommendations found.")
    return
  columns = st.columns(df.shape[0])
  items = df.to_dict(orient='records')
  any(tile_item(c, i) for c, i in zip(columns, items))
