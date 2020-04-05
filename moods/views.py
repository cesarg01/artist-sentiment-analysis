from django.shortcuts import render
from spotify import Spotify
# Create your views here.

def index_page(request):

    #sp = Spotify()
    context = {}

    if(request.method == 'POST'):
        artist_name = request.POST.get('artist_search', '')
        context['artist_name'] = artist_name


    
    return render(request, 'moods/index.html', context)