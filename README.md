# MovieCafe AI - Movie Recommender System 🍿

[![Live Demo](https://img.shields.io/badge/Live_Demo-moverecommenderapp.netlify.app-00C7B7?style=for-the-badge&logo=netlify)](https://moverecommenderapp.netlify.app)
[![Backend API](https://img.shields.io/badge/API-Render-46E3B7?style=for-the-badge&logo=render)](https://movie-recommendor-g09x.onrender.com)
[![Expo](https://img.shields.io/badge/Frontend-Expo_React_Native-000020?style=for-the-badge&logo=expo)](https://expo.dev/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

A full-stack, machine learning-powered movie recommendation platform. MovieCafe AI uses content-based filtering to suggest personalized cinematic masterpieces based on user preferences.

## 🌟 Features
- **Smart Recommendations:** Uses Scikit-learn and Cosine Similarity to analyze movie features (genres, keywords, cast, crew) and predict similar films.
- **Cross-Platform Frontend:** Built with React Native (Expo) for a seamless, responsive experience.
- **High-Performance API:** Backend served via FastAPI, providing fast and reliable recommendation queries.
- **Dynamic Content:** Integrates with the TMDB REST API to fetch high-quality movie posters and real-time metadata.

## 🏗️ Architecture
This project is built using a modern microservices architecture:
* **Machine Learning:** `scikit-learn`, `pandas`, `numpy`
* **Backend API:** Python, `FastAPI`, `uvicorn` (Deployed on **Render**)
* **Frontend Web App:** React Native, Expo, Axios, TailwindCSS (Deployed on **Netlify**)

## 🚀 Live Demo
You can try out the application live here:
👉 **[MovieCafe AI Live Web App](https://moverecommenderapp.netlify.app)**

*(Note: The backend API is hosted on Render's free tier. If the app hasn't been used in 15 minutes, the first search may take up to 45 seconds to wake up the server. Subsequent searches are instant!)*

## 💻 Local Setup & Installation

To run this project locally on your machine, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/vaishnavithulir/movie-recommendor.git
cd movie-recommendor
```

### 2. Setup the FastAPI Backend
```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Start the FastAPI server
uvicorn backend.main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 3. Setup the Expo Frontend
```bash
# Navigate to the mobile app directory
cd mobile_app

# Install dependencies
npm install

# Update the API URL
# In mobile_app/backend_config.ts, change API_URL to 'http://localhost:8000' for local testing.

# Start the development server
npm start
```
*Press `w` in the terminal to open the web version in your browser.*

## 🧠 How the Recommendation Engine Works
The recommendation system uses **Content-Based Filtering**. It works on the principle that if you like a particular item, you will also like items that are similar to it. 
1. We process a dataset of 5000+ movies to extract tags combining genres, keywords, cast, and directors.
2. We use text vectorization techniques to convert these tags into numerical vectors.
3. We calculate the **Cosine Similarity** between these vectors to determine the mathematical distance between different movies.
4. When a user searches for a movie, the system instantly returns the 5 closest movies in the vector space.

---
*Built by [Vaishnavi Thulir](https://github.com/vaishnavithulir)*
