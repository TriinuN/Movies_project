# moviesearch/views.py
from django.shortcuts import render, get_object_or_404
from django.views import View
from .forms import MovieSearchForm
import requests

TMDB_API_KEY = 'b47270d2fdc04dcc59d65d891dab043a'
TMDB_API_URL = 'https://api.themoviedb.org/3/search/movie'
MOVIE_DETAIL_API_URL = 'https://api.themoviedb.org/3/movie/'
GENRES_API_URL = 'https://api.themoviedb.org/3/genre/movie/list'

class MovieSearchView(View):
    def get(self, request):
        form = MovieSearchForm()
        return render(request, 'moviesearch/search.html', {'form': form})

    def post(self, request):
        form = MovieSearchForm(request.POST)
        movie_results = []
        if form.is_valid():
            title = form.cleaned_data['title']
            response = requests.get(TMDB_API_URL, params={
                'api_key': TMDB_API_KEY,
                'query': title
            })
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    genre_names = self.get_genre_names()
                    movie_results = []
                    for movie in data['results']:
                        genre_list = [genre_names.get(id, 'Unknown') for id in movie.get('genre_ids', [])]
                        movie_results.append({
                            'id': movie.get('id'),
                            'title': movie.get('title'),
                            'year': movie.get('release_date', '')[:4],
                            'genre': ', '.join(genre_list),
                            'overview': movie.get('overview'),
                            'poster_path': movie.get('poster_path') if movie.get('poster_path') else 'default_image.jpg'
                        })
        return render(request, 'moviesearch/search.html', {'form': form, 'movie_results': movie_results})

    def get_genre_names(self):
        response = requests.get(GENRES_API_URL, params={'api_key': TMDB_API_KEY})
        if response.status_code == 200:
            data = response.json()
            return {genre['id']: genre['name'] for genre in data['genres']}
        return {}

class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = self.get_movie_details(movie_id)
        return render(request, 'moviesearch/movie_detail.html', {'movie': movie})

    def get_movie_details(self, movie_id):
        response = requests.get(f'{MOVIE_DETAIL_API_URL}{movie_id}', params={'api_key': TMDB_API_KEY})
        if response.status_code == 200:
            movie = response.json()
            genre_names = self.get_genre_names()
            genre_list = [genre_names.get(id, 'Unknown') for id in movie.get('genres', [])]
            return {
                'title': movie.get('title'),
                'year': movie.get('release_date', '')[:4],
                'genre': ', '.join(genre_list),
                'overview': movie.get('overview'),
                'poster_path': movie.get('poster_path') if movie.get('poster_path') else 'default_image.jpg'
            }
        return {}

    def get_genre_names(self):
        response = requests.get(GENRES_API_URL, params={'api_key': TMDB_API_KEY})
        if response.status_code == 200:
            data = response.json()
            return {genre['id']: genre['name'] for genre in data['genres']}
        return {}
