from bs4 import BeautifulSoup
import requests
import re
import time


# genius url is artist/song (ex. https://genius.com/Gojira-stranded-lyrics )
song_url = 'https://genius.com/{}-{}-lyrics'

def get_song_lyrics(artist_name, song_name):
    '''
        Scrape genius for lyrics to specified song.
    '''

    a_name = artist_song_url_checker(artist_name)
    s_name = artist_song_url_checker(song_name)
    #print(a_name)
    #print(s_name)

    if(len(a_name) == 0 or len(s_name) == 0):
        return

    url = song_url.format(a_name, s_name)
    print(url)
    song = {}
    song['name'] = song_name
    song_lyrics = scrape(url, song)
    

    return song_lyrics

def scrape(url, song):
    '''
        Scrape genius and add lyrics to the dictionary.
        NOTE: Need to add sleep function and some songs may not have lyrics. Add a check for lyrics.
    '''
    genius_site_object = requests.get(url)
    genius_site_text = genius_site_object.text

    genius_site_soup = BeautifulSoup(genius_site_text, 'html.parser')

    # Get lyrics
    for song_lyric in genius_site_soup.find_all('div', class_= 'song_body-lyrics'):
        # Strip off all the whitespace
        lyrics = song_lyric.get_text().rstrip().strip()
        # Delete the first 4 lines
        old_lyrics = lyrics.split('\n')[4:]
        # Delete the last 6 lines
        new_lyrics = old_lyrics[:len(old_lyrics)-6]
        post_lyrics = '\n'.join(map(str, new_lyrics))
        song['lyrics'] = post_lyrics#''.join(post_lyrics)
        #print(song)

    return song



def artist_song_url_checker(phrase):
    '''
        Create a friendlier artist and song name text for the url address.
    '''
    # The unicode characters are the single left and right quotation marks followed
    # by the left and right double quotation marks.
    res = phrase.lower() \
        .replace(u'\u2018', '') \
        .replace(u'\u2019', '') \
        .replace(u'\u201c', '') \
        .replace(u'\u201d', '') \
        .replace('$', 's') \
        .replace('&', 'and') \
        .replace('.', '') \
        .replace('\'', '') \
        .replace(',', '') \
        .replace('.', '') \
        .replace('?', '') \
        .replace('/', '') \
        .replace('!', '') \
        .replace(' ', '-')
    # remove "()" section (ex. "(feat. J Cole)")
    if '(' in res:
        res = res[:res.find('(') - 1].strip()
    return res.replace('--', '-')



