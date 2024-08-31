from django.urls import path
from .views import MovieDetailView, SaveMovieView, SavedMoviesView

app_name = 'moviedetails'
urlpatterns = [
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
    path('save/<int:movie_id>/', SaveMovieView.as_view(), name='save_movie'),
    path('saved_movie/', SavedMoviesView.as_view(), name='saved_movies'),
]
