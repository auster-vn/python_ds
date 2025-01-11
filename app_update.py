from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import os
import requests
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
api_key = os.getenv("API_KEY")

app = Flask(__name__)

# Load TMDb datasets
movies_file = './data/tmdb_5000_movies.csv'
credits_file = './data/tmdb_5000_credits.csv'

# Read CSV files
df_movies = pd.read_csv(movies_file)
df_credits = pd.read_csv(credits_file)

# Rename columns for clarity
df_credits.rename(columns={'title': 'movie_title', 'movie_id': 'id'}, inplace=True)

# Merge datasets on 'id' column
merged_df = pd.merge(df_movies, df_credits, on='id')

# Select relevant columns and clean data
df = merged_df[['id', 'movie_title', 'vote_average', 'vote_count', 'runtime', 'genres', 'cast']]

# Ensure numeric columns are properly converted
df['vote_average'] = pd.to_numeric(df['vote_average'], errors='coerce')
df['vote_count'] = pd.to_numeric(df['vote_count'], errors='coerce')
df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce')

# Process genres and cast columns
def process_json_column(json_column):
    try:
        data = eval(json_column)
        return [item['name'] for item in data]
    except:
        return []

df['genres'] = df['genres'].apply(process_json_column)
df['cast'] = df['cast'].apply(process_json_column)

# Generate movie titles for the datalist
movie_titles = df['movie_title'].tolist()

# Cache for storing fetched posters
poster_cache = {}

# Function to fetch poster from TMDb API with caching
def fetch_poster(movie_id):
    if movie_id in poster_cache:
        return poster_cache[movie_id]
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url).json()
    poster_path = response.get('poster_path')
    poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/150"
    
    # Store the fetched poster in cache
    poster_cache[movie_id] = poster_url
    return poster_url

# Search function
def search_movies(query, min_rating=0):
    matching_movies = df[
        df['movie_title'].str.contains(query, case=False, na=False) &
        (df['vote_average'] >= min_rating)
    ]
    results = []
    for _, movie in matching_movies.iterrows():
        poster_url = fetch_poster(movie['id'])
        results.append({
            'title': movie['movie_title'],
            'poster_path': poster_url,
            'vote_average': movie['vote_average']
        })
    return results

@app.route('/')
def home():
    return render_template('index.html', movie_list=movie_titles, search_query="", rating_filter=0)

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get form data
    movie_name = request.form['movie_name']
    min_rating = float(request.form['rating'])
    # Search for matching movies
    recommendations = search_movies(movie_name, min_rating)
    return render_template(
        'index.html',
        movie_list=movie_titles,
        recommendations=recommendations,
        search_query=movie_name,
        rating_filter=min_rating
    )

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

@app.route('/documents')
def documents():
    doc_folder = './static/doc'
    files = os.listdir(doc_folder)
    return render_template('documents.html', files=files)

@app.route('/doc/<filename>')
def serve_pdf(filename):
    return send_from_directory('./static/doc', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5001)

