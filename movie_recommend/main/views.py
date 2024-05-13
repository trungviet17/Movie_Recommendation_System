from django.shortcuts import render, get_object_or_404
from .models import Movie, Cast
from django.contrib.auth.decorators import login_required
# Create your views here.


# @login_required
def home(request): 
    return render(request, 'main/home.html')

@login_required
def recommend(request, movie_id): 
    movie = get_object_or_404(Movie, id = movie_id)
    casts = movie.casts.all()
    return render(request, 'main/recommend.html', {'movie' : movie, 'casts' : casts})

@login_required
def search(request): 
    movies = None 
    if request.method == 'POST': 
        search = request.POST['search']

        movies = Movie.objects.filter(title__icontains = search)

        if movies != None : 
            return render(request, 'main/search.html', {'movies': movies, 'search' : search})
   
    return render(request, 'main/search.html', {})
def test(request):
    return render(request, 'main/recommend.html')