'''
Author: Bappy Ahmed
Email: entbappy73@gmail.com
Date: 2021-Nov-15
Updated by: Malhar Nikam
Modified for MovieCafe Theme and API Fixes by Assistant
'''

import pickle
import streamlit as st
import requests
import pandas as pd

def fetch_poster(movie_id):
    """Fetches the movie poster URL from TMDB API."""
    url = "https://api.tmdb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=5)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
    except requests.exceptions.RequestException:
        pass
    return "https://placehold.co/500x750/333/FFFFFF?text=No+Poster"


def recommend(movie):
    """Recommends 5 similar movies based on the selected movie."""
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        st.error("Movie not found in the dataset. Please select another one.")
        return [], [], [], []
        
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_years = []
    recommended_movie_ratings = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_years.append(movies.iloc[i[0]].year)
        recommended_movie_ratings.append(movies.iloc[i[0]].vote_average)

    return recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings


st.set_page_config(page_title="MovieCafe Recommender", layout="wide", page_icon="🍿")

# --- CUSTOM MOVIECAFE STYLE ---
st.markdown("""
<style>
/* Pro Cinema Background using Unsplash image to avoid CORS/404s */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(to bottom, rgba(10, 10, 10, 0.7) 0%, rgba(10, 10, 10, 0.95) 100%), 
                url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop') no-repeat center center fixed !important;
    background-size: cover !important;
    color: white;
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* MovieCafe Logo-like Title */
h1 {
    color: #ff3333 !important;
    font-weight: 900 !important;
    font-size: 3.5rem !important;
    text-align: center;
    margin-bottom: 5px;
    letter-spacing: 1px;
    text-shadow: 0px 4px 15px rgba(255, 51, 51, 0.4);
    text-transform: uppercase;
}

/* Subtitle styling */
.subtitle {
    font-size: 1.15rem;
    font-weight: 400;
    text-align: center;
    color: #dddddd;
    margin-bottom: 40px;
    letter-spacing: 0.5px;
}

/* Selectbox styling */
div[data-baseweb="select"] > div {
    background-color: rgba(30, 30, 30, 0.8) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.15) !important;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    padding: 2px;
}
div[data-baseweb="select"] * {
    color: white !important;
}

/* The red primary button */
.stButton {
    display: flex;
    justify-content: center;
    margin-top: 10px;
}
.stButton > button {
    background: linear-gradient(90deg, #ff3333 0%, #cc0000 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 30px !important;
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    width: 60% !important; /* Keep button constrained nicely */
    box-shadow: 0 4px 15px rgba(255, 51, 51, 0.3);
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 51, 51, 0.6);
}

/* Poster Hover Effects */
img {
    border-radius: 12px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.8);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    border: 2px solid transparent;
}
img:hover {
    transform: scale(1.08) translateY(-10px);
    border: 2px solid #ff3333;
    cursor: pointer;
    box-shadow: 0 15px 30px rgba(255, 51, 51, 0.3);
}

/* Captions & Text */
div[data-testid="stText"] {
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    text-align: center !important;
    color: #ffffff !important;
    margin-top: 20px !important;
    text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}
div[data-testid="stCaptionContainer"] {
    font-size: 0.95rem !important;
    text-align: center !important;
    color: #aaaaaa !important;
}

/* Centered content spacing */
.block-container {
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

</style>
""", unsafe_allow_html=True)


# Load the data files
try:
    movies_dict = pickle.load(open('artifacts/movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model files not found. Please run the data processing notebook first.")
    st.stop()


movie_list = movies['title'].values

# Hero Section
st.markdown("<h1>MovieCafe AI Recommender</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Discover your next cinematic masterpiece</p>", unsafe_allow_html=True)

# Organize layout properly using columns to make it look professional
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    selected_movie = st.selectbox("", movie_list, label_visibility="collapsed", placeholder="Search for a movie...")
    
    st.write("") # small spacing
    if st.button('Show Recommendations', use_container_width=True):
        show_recs = True
    else:
        show_recs = False

if show_recs:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.spinner('MovieCafe is finding the best matches for you...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_years, recommended_movie_ratings = recommend(selected_movie)
    
    if recommended_movie_names:
        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.image(recommended_movie_posters[i], use_container_width=True)
                st.text(recommended_movie_names[i])
                year = recommended_movie_years[i]
                if pd.notna(year):
                    st.caption(f"Year: {int(year)}")
                rating = recommended_movie_ratings[i]
                st.caption(f"Rating: {rating:.1f} ⭐")
