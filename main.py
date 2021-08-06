from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import re

def get_info(artist_name, page):
    base_url = 'https://api.genius.com'
    access_token = 'u9Y8tPQWDHXFRKSSYArtObxN1gbc_HTdyfx4y3rMyVb6jJOCPA3qkHVI4SNC3Pcx'
    headers = {'Authorization': 'Bearer ' + access_token}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


def get_urls(artist_name):
    page = 1
    num_of_songs = [0]
    song_urls = []

    while True:
        response = get_info(artist_name, page)
        json = response.json()

        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                    song_info.append(hit)
        


        for song in song_info:
                song_urls.append(song['result']['url'])
        print(len(song_urls))

        num_of_songs.append(len(song_urls))
        if num_of_songs[-1] == num_of_songs[-2]:
            break
        else:
            page += 1

    return song_urls


def scrape_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    lyrics = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-8 eOLwDW')
    lyrics = ''.join(re.sub('\[(.*?)\]', '', section.get_text(" ")) for section in lyrics)
    return lyrics

def write_lyrics_to_file(artist_name):
    f = open(f'{artist_name}.txt', 'w+', encoding='utf-8')
    urls = get_urls(artist_name)
    for url in urls:
        lyrics = scrape_lyrics(url)
        f.write(lyrics)
    f.close()
