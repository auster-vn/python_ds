
## Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/auster-vn/MOVIE-RECOMMENDATION-SYSTEM.git
    cd MOVIE-RECOMMENDATION-SYSTEM
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the [.env](http://_vscodecontentref_/15) file with your TMDb API key:
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

## Team Members

- Tran Chau Phu (MSSV: 22110158)
- Ho Minh Quan (MSSV: 22110170)
- Le Nguyen Duc Nam (MSSV: 22110123)
- Le Thi Kim Nga (MSSV: 22110124)
- Tran Nguyen Thanh Phong (MSSV: 22110155)

## License

This project is licensed under the MIT License.