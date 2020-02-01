from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Movie, Seed
from django.db.models import Q


# Create your views here.
def index(request):
    item_list = Movie.objects.order_by('-id')[:50]
    for item in item_list:
        item.actor = ','.join(item.actor.split(',')[0:4])
    context = {'item_list': item_list}
    return render(request, 'movie/index.html', context)


def list(request):
    movie_list = Movie.objects.filter(is_movie=True).order_by('-id')
    paginator = Paginator(movie_list, 25)
    page = request.GET.get('page')
    movie_list = paginator.get_page(page)
    context = {'movie_list': movie_list}
    return render(request, 'movie/list.html', context)


def tv_list(request):
    movie_list = Movie.objects.filter(is_movie=False).order_by('-id')
    paginator = Paginator(movie_list, 25)
    page = request.GET.get('page')
    movie_list = paginator.get_page(page)
    context = {'movie_list': movie_list}
    return render(request, 'movie/tv_list.html', context)


def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    seed_list = Seed.objects.filter(imdb=movie.imdb)
    movie.actor = movie.actor.split(",")
    movie.writer = movie.writer.split(",")
    movie.director = movie.director.split(",")

    context = {
        'movie': movie,
        'seed_list': seed_list,
    }
    return render(request, 'movie/detail.html', context)

def search(request):
    query = request.GET.get('q')
    movie_list = Movie.objects.filter(
        Q(name__contains=query) | Q(name_en__contains=query)
        | Q(fullname__contains=query))
    context = {'movie_list': movie_list, 'query': query}
    for m in movie_list:
        m.name = m.name.replace(query, "<b>" + query + "</b>")
        m.name_en = m.name_en.replace(query, "<b>" + query + "</b>")
        m.fullname = m.fullname.replace(query, "<b>" + query + "</b>")
    return render(request, 'movie/search.html', context)


def people(request):
    query = request.GET.get('q')
    movie_list = Movie.objects.filter(
        Q(actor__contains=query) | Q(writer__contains=query)
        | Q(director__contains=query))
    context = {'movie_list': movie_list, 'query': query}
    for m in movie_list:
        m.actor = m.actor.replace(query, "<b>" + query + "</b>")
        m.writer = m.writer.replace(query, "<b>" + query + "</b>")
        m.director = m.director.replace(query, "<b>" + query + "</b>")
    return render(request, 'movie/people.html', context)


def about(request):
    return render(request, 'movie/about.html')
