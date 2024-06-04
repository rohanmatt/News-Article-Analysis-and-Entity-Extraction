import streamlit as st
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import spacy
from gensim import corpora, models

import streamlit as st

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

# Download required NLTK data
nltk.download('stopwords')
nltk.download('punkt')

# Text preprocessing
def preprocess_text(text):
    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)
    
    # Tokenize text
    tokens = word_tokenize(text.lower())
    
    # Remove stopwords and stem tokens
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    filtered_tokens = [ps.stem(token) for token in tokens if token not in stop_words]
    
    return filtered_tokens

# Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")

def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))
    return entities

# Topic Modeling
def topic_modeling(texts):
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    # Train LDA model
    lda_model = models.LdaMulticore(corpus=corpus, id2word=dictionary, num_topics=10)
    
    return lda_model.print_topics()

# Streamlit app
def main():
    st.title("News Article Analysis and Entity Extraction")

    # Sidebar
    st.sidebar.title("Options")
    option = st.sidebar.radio("Choose an option", ["Text Input", "File Upload"])

    if option == "Text Input":
        article_text = st.text_area("Enter news article text")
        if st.button("Analyze"):
            if article_text:
                preprocessed_text = preprocess_text(article_text)
                entities = extract_entities(article_text)
                st.write("Entities:", entities)

                documents = [preprocessed_text]
                topics = topic_modeling(documents)
                st.write("Topics:", topics)
            else:
                st.warning("Please enter some text to analyze.")

    elif option == "File Upload":
        uploaded_file = st.file_uploader("Upload a news article file", type=["txt"])
        if uploaded_file is not None:
            article_text = uploaded_file.read().decode("utf-8")
            preprocessed_text = preprocess_text(article_text)
            entities = extract_entities(article_text)
            st.write("Entities:", entities)

            documents = [preprocessed_text]
            topics = topic_modeling(documents)
            st.write("Topics:", topics)

if __name__ == "__main__":
    main()