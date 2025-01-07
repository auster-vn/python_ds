from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import pickle
import os
import requests
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

app = Flask(__name__)

# Load Data
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Load ratings and additional details from CSV
df_ratings = pd.read_csv('data/data.csv', encoding='utf-8')
df_ratings['vote_average'] = pd.to_numeric(df_ratings['vote_average'], errors='coerce')
df_ratings['vote_count'] = pd.to_numeric(df_ratings['vote_count'], errors='coerce')
df_ratings['runtime'] = pd.to_numeric(df_ratings['runtime'], errors='coerce')

# Cache for storing fetched posters
poster_cache = {}

def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id]
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/150"
    poster_cache[movie_id] = poster_url
    
    return poster_url

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
    except IndexError:
        return []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        movie_title = movies.iloc[i[0]].title
        rating_info = df_ratings[df_ratings['id'] == movie_id].iloc[0] if movie_id in df_ratings['id'].values else None
        
        recommended_movies.append({
            'title': movie_title,
            'poster_path': fetch_poster(movie_id),
            'vote_average': rating_info['vote_average'] if rating_info is not None else "N/A",
            'vote_count': rating_info['vote_count'] if rating_info is not None else "N/A",
            'runtime': rating_info['runtime'] if rating_info is not None else "N/A"
        })
    return recommended_movies

# Home Route
@app.route('/')
def home():
    return render_template('index.html', movie_list=movies['title'].tolist(), recommendations=[])

# Recommendation Route
@app.route('/recommend', methods=['POST'])
def recommend_movies():
    movie_name = request.form['movie_name']
    recommendations = recommend(movie_name)
    return render_template(
        'index.html',
        movie_list=movies['title'].tolist(),
        recommendations=recommendations,
        search_query=movie_name
    )

# Members Route
@app.route('/members')
def members():
    team_members = [
        {"MSSV": "22110158", "Hovaten": "Tran Chau Phu"},
        {"MSSV": "22110170", "Hovaten": "Ho Minh Quan"},
        {"MSSV": "22110123", "Hovaten": "Le Nguyen Duc Nam"},
        {"MSSV": "22110124", "Hovaten": "Le Thi Kim Nga"},
        {"MSSV": "22110155", "Hovaten": "Tran Nguyen Thanh Phong"},
    ]
    return render_template('members.html', members=team_members)

# Documents Route
@app.route('/documents')
def documents():
    doc_folder = './static/doc'
    files = os.listdir(doc_folder)
    return render_template('documents.html', files=files)

@app.route('/doc/<filename>')
def serve_pdf(filename):
    return send_from_directory('./static/doc', filename)

if __name__ == '__main__':
    app.run(debug=True)

