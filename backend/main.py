import pickle
import pandas as pd
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import os

app = FastAPI(title="Movie Recommender API")

# Enable CORS for mobile app connectivity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Constants
TMDB_API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Global data variables
movies = None
similarity = None

def load_data():
    global movies, similarity
    try:
        # Render has the code in the root directory
        movie_dict_path = "artifacts/movie_dict.pkl"
        similarity_path = "artifacts/similarity_small.pkl"
        
        print(f"Loading data from: {movie_dict_path}")
        with open(movie_dict_path, 'rb') as f:
            movies_dict = pickle.load(f)
        movies = pd.DataFrame(movies_dict)
        
        with open(similarity_path, 'rb') as f:
            similarity = pickle.load(f)
        print("Data loaded successfully")
    except Exception as e:
        print(f"Error loading data: {e}")

@app.get("/health")
async def health():
    return {"status": "ok", "data_loaded": movies is not None}

@app.get("/")
async def root():
    return {"message": "Movie Recommender API is running"}

@app.on_event("startup")
async def startup_event():
    load_data()

class Movie(BaseModel):
    id: int
    title: str
    poster_url: str
    year: Optional[int]
    rating: float

class RecommendationResponse(BaseModel):
    recommendations: List[Movie]

def fetch_poster(movie_id):
    url = f"https://api.tmdb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        data = requests.get(url, timeout=5)
        data.raise_for_status()
        data = data.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except:
        pass
    return "https://placehold.co/500x750/333/FFFFFF?text=No+Poster"

@app.get("/movies")
def get_movies():
    if movies is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    return movies[['movie_id', 'title']].to_dict(orient='records')

import numpy as np

@app.get("/recommend/{movie_title}", response_model=RecommendationResponse)
def get_recommendations(movie_title: str):
    if movies is None or similarity is None:
        raise HTTPException(status_code=500, detail="Data not loaded")
    
    try:
        # Match title
        search_title = movie_title.strip().lower()
        idx_list = movies[movies['title'].str.lower() == search_title].index
        if len(idx_list) == 0:
            raise HTTPException(status_code=404, detail=f"Movie '{movie_title}' not found")
        
        index = idx_list[0]
        
        # Memory-efficient similarity calculation
        sim_scores = similarity[index]
        movie_indices = np.argsort(sim_scores)[::-1][1:7]
        
        recs = []
        for i in movie_indices:
            movie_row = movies.iloc[i]
            
            m_id = int(movie_row.get('movie_id', 0))
            m_title = str(movie_row.get('title', 'Unknown'))
            m_year = movie_row.get('year')
            m_rating = movie_row.get('vote_average', 0.0)
            
            recs.append(Movie(
                id=m_id,
                title=m_title,
                poster_url=fetch_poster(m_id),
                year=int(m_year) if pd.notna(m_year) else None,
                rating=float(m_rating) if pd.notna(m_rating) else 0.0
            ))
            
        return {"recommendations": recs}
    except Exception as e:
        print(f"CRASH in get_recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
