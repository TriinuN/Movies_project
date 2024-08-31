from django import forms


class SaveMovieForm(forms.Form):
    movie_id = forms.IntegerField()
    title = forms.CharField(max_length=255)
    year = forms.CharField(max_length=4)
    genre = forms.CharField(max_length=255, required=False)
    overview = forms.CharField(widget=forms.Textarea, required=False)
    poster_path = forms.CharField(max_length=255, required=False)
