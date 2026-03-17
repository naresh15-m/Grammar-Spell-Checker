import pickle as pk
import streamlit as st

# Load the entire pipeline
pipeline = pk.load(open('pipeline.pkl', 'rb'))

st.title("Movie Review Sentiment Analysis")
review = st.text_input('Enter Movie Review')

if st.button('Predict'):
    if review.strip() == "":
        st.warning("Please enter a review!")
    else:
        # The pipeline handles preprocessing automatically
        result = pipeline.predict([review])
        
        if result[0] == 0:
            st.error('Negative Review 😞')
        else:
            st.success('Positive Review 😊')