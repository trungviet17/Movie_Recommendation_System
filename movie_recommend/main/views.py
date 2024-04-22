from django.shortcuts import render, get_object_or_404
from .models import Movie, Cast
# Create your views here.



def home(request): 
    return render(request, 'main/home.html')


def recommend(request, movie_id): 
    movie = get_object_or_404(Movie, id = movie_id)
    casts = movie.casts.all()
    return render(request, 'main/recommend.html', {'movie' : movie, 'casts' : casts})


def search(request): 
    movies = None 
    if request.method == 'POST': 
        search = request.POST['search']

        movies = Movie.objects.filter(title__contains = search)

        if movies != None : 
            return render(request, 'main/search.html', {'movies': movies, 'search' : search})
   
    return render(request, 'main/search.html', {})