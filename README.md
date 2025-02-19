# Movie Recommendation System

This is a Flask-based web application that provides movie recommendations based on user input. The application uses data from TMDb and a pre-trained model to suggest similar movies.

## Features

- Search for movies by title
- Filter search results by minimum rating
- View movie details including poster, rating, and runtime
- View team members
- Access project documents

## Project Structure


## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/auster-vn/python_ds
    cd MOVIE-RECOMMENDATION-SYSTEM
    ```

2. Create and activate a Conda environment:
    ```sh
    conda create --name movie-recommender python=3.8
    conda activate movie-recommender
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the [.env](http://_vscodecontentref_/16) file with your TMDb API key:
    ```
    API_KEY=your_tmdb_api_key
    ```

5. Run the application:
    ```sh
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5001` to access the application.

## Usage

- Enter a movie name in the search bar and click "Search Movies" to get recommendations.
- Use the rating filter to narrow down the search results.
- Click on a movie poster to view more details about the movie.


## License

This project is licensed under the MIT License.
