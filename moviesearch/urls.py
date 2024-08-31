from django.urls import path
from .views import MovieSearchView, MovieDetailView

urlpatterns = [
    path('', MovieSearchView.as_view(), name='search_movie'),
    path('movie/<int:movie_id>/', MovieDetailView.as_view(), name='movie_detail'),
]
