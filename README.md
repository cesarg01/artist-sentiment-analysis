# Artist Sentiment Analysis
Project that analyzes the sentiment (mood) of the albums from the user inputted artist. One will be able to see how 
the mood changes from album to album and where each song is in the scale (Happy, Neutral, or Dark).

## Updates
There is a graph not showing up issue when searching for artists who have 10+ songs in their albums. This issue could be fixed by
using the Fetch function in main.js file. Another possible fix is using Threads to speed up the web scraping process. 

### Built With

* [Django](https://docs.djangoproject.com/en/2.1/) - Web Framework
* [Spotipy](https://github.com/plamere/spotipy) - Spotify Python Wrapper API
* [Spotify API](https://developer.spotify.com/) - Used to get Developer key
* [ChartJS](https://www.chartjs.org/) - Modern Graph
* [TextBlob](https://github.com/sloria/textblob) - API for common NLP tasks