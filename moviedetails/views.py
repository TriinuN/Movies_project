from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import requests
from django.views import View
from .models import SavedMovie


TMDB_API_KEY = 'b47270d2fdc04dcc59d65d891dab043a'
MOVIE_DETAIL_API_URL = 'https://api.themoviedb.org/3/movie/'
GENRES_API_URL = 'https://api.themoviedb.org/3/genre/movie/list'


class MovieDetailView(View):
    def get(self, request, movie_id):
        movie = self.get_movie_details(movie_id)
        if movie:
            return render(request, 'moviedetails/movie_details.html', {'movie': movie})
        else:
            return render(request, 'moviedetails/movie_details.html', {'error': 'Movie not found'})

    def get_movie_details(self, movie_id):
        response = requests.get(f'{MOVIE_DETAIL_API_URL}{movie_id}', params={'api_key': TMDB_API_KEY})
        if response.status_code == 200:
            movie = response.json()
            return {
                'title': movie.get('title'),
                'year': movie.get('release_date', '')[:4],
                'genre': ', '.join(genre['name'] for genre in movie.get('genres', [])),
                'overview': movie.get('overview'),
                'poster_path': movie.get('poster_path'),
                'cast': self.get_movie_cast(movie_id)
            }
        return None

    def get_movie_cast(self, movie_id):
        response = requests.get(f'{MOVIE_DETAIL_API_URL}{movie_id}/credits', params={'api_key': TMDB_API_KEY})
        if response.status_code == 200:
            cast_data = response.json()
            return [actor['name'] for actor in cast_data.get('cast', [])[:5]]
        return []


class SaveMovieView(View):
    def post(self, request, movie_id):
        if request.user.is_authenticated:
            SavedMovie.objects.create(
                user=request.user,
                movie_id=movie_id,
                movie_title=request.data.get('movie_title'),
                movie_poster=request.POST.get('movie_poster')
            )
        return redirect('movie_detail', movie_id=movie_id)


class SavedMoviesView(View):
    @login_required
    def get(self, request):
        if not request.user.is_authenticated:
            print("User is not authenticated")
        saved_movies = SavedMovie.objects.filter(user=request.user)
        return render(request, 'moviedetails/saved_movies.html', {'saved_movies': saved_movies})