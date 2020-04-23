from django.shortcuts import render
from django.http import HttpResponse
from spotify import Spotify
import json
# Create your views here.

def index_page(request):

    sp = Spotify()
    context = {}

    if(request.method == 'POST'):
        artist_name = request.POST.get('artist_search', '')
        context['artist_name'] = artist_name
        results = sp.get_artist(context['artist_name'])
        
       
        context['results'] = results['albums'][0]['songs']
        context['artist_data'] = json.dumps(results)
        context['blind'] = results['albums'][0]['songs'][0]['polarity']


    
    return render(request, 'moods/index.html', context)