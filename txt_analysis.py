from PIL import Image
import numpy as np
import pandas as pd
import altair as alt
import re
import nltk
from collections import Counter
from nltk.tokenize import word_tokenize
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from io import StringIO
nltk.download('punkt')

st.write('## Analyzing Top Netflix Movie Reviews')
st.sidebar.header("Word Cloud Settings")
max_word = st.sidebar.slider("Max Words",10,200,100,10)
max_font = st.sidebar.slider("Size of Largest Word",50,350,60)
image_size = st.sidebar.slider("Image Width",100,800,400,10)
random = st.sidebar.slider("Random State",30,100,42)
stopword_check = st.sidebar.checkbox('Remove Stop Words', value=False)

st.sidebar.header("Word Count Settings")
min_word = st.sidebar.slider("Minimum count of Words",10,200,40,10)
#define a function to set stopwords
stopwords = set(STOPWORDS)
def set_stopwords():
    if stopword_check:
        stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
        'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
        'put', 'seem', 'asked', 'made', 'half', 'much',
        'certainly', 'might', 'came','\'s','n\'t','\'ve','\'re','\'m'])
        return stopwords
    else:
        return stopwords
# Create a dictionary with key/value pair to associate with the selectbox
books = {" ":" ","Stranger Things":"data/stranger.csv","Money Heist":"data/heist.csv","Squid Game":"data/squid.csv"}
#define a function to pass the selected book
def select_func(selected_book):
    return books[selected_book]

selected_book = st.selectbox("Select a Movie", books)

if selected_book !=' ':
    try:
        with open(select_func(selected_book)) as input:
            dataset = input.read()
    except FileNotFoundError:
            st.error('File not found.')

tab1, tab2, tab3 = st.tabs(['Word Cloud','Bar Chart','View Text'])

with tab1:
    if selected_book !=' ':
        cloud = WordCloud(background_color = "white", 
                            max_words = max_word, 
                            max_font_size=max_font,
                            stopwords = set_stopwords(), 
                            random_state=random)
        wc = cloud.generate(dataset)
        word_cloud = cloud.to_file('wordcloud.png')
        st.image(wc.to_array(), width = image_size)

with tab2:
    if selected_book !=' ':
        try:
            with open(select_func(selected_book)) as input:
                stringoutput = input.read()
                stringoutput = stringoutput.lower()
                #stringoutput = stringoutput.translate(str.maketrans('','',string.punctuation))
                stringoutput = word_tokenize(stringoutput)
                remPunc = re.compile('.*[A-Za-z].*')
                filtered = [t for t in stringoutput if remPunc.match(t)] 
                filtered = [t for t in filtered if not t in set_stopwords()]
                counts = Counter(filtered)
                frequency = nltk.FreqDist(counts)
                freq_df = pd.DataFrame(frequency.items(),columns=['word','count'])
                barPlot = alt.Chart(freq_df).transform_filter(
                alt.FieldGTEPredicate(field='count', gte=min_word)).mark_bar().encode(
                    x='count',
                    y=alt.Y('word',sort='-x')
                )
                st.altair_chart(barPlot, use_container_width=True)
        except FileNotFoundError:
            st.error('File not found.')

with tab3:
    if selected_book !=' ':
        try:
            with open(select_func(selected_book)) as input:
                stringio = input.read()
                st.header(selected_book)
                st.write(stringio)
        except FileNotFoundError:
                st.error('File not found.')