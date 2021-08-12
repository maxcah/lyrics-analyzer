from bs4 import BeautifulSoup
from nltk.corpus import wordnet as wn
import requests
import re
import matplotlib.pyplot as plt
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
Config.set('graphics', 'width', '192')
Config.set('graphics', 'height', '108')
Config.set('graphics', 'resizable', False)


# Gets info on the given artist from Genius API
def get_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    access_token = 'u9Y8tPQWDHXFRKSSYArtObxN1gbc_HTdyfx4y3rMyVb6jJOCPA3qkHVI4SNC3Pcx'
    headers = {'Authorization': 'Bearer ' + access_token}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response


# Returns a list of Genius URLs of all the artist's songs
def get_song_urls(artist_name):
    page = 1
    num_of_songs = [0]
    song_urls = []

    while True:
        response = get_artist_info(artist_name, page)
        json = response.json()

        # Collects all Genius URLs of the artist's songs
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_urls.append(hit['result']['url'])

        # Breaks if no new songs were added, if not goes on to the next page
        num_of_songs.append(len(song_urls))
        if num_of_songs[-1] == num_of_songs[-2]:
            break
        else:
            page += 1

    return song_urls


# Scrapes lyrics from Genius URLs
def scrape_lyrics(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    lyrics = soup.find_all('div', class_='Lyrics__Container-sc-1ynbvzw-8 eOLwDW')
    lyrics = ''.join(re.sub('\[(.*?)\]', '', section.get_text(" ").lower()) for section in lyrics)
    return re.sub('[?,!)(:;]', '', lyrics)


# Writes all the lyrics to a file
def write_lyrics_to_file(artist_name):
    f = open(f'{artist_name.lower()}.txt', 'w+', encoding='utf-8')
    urls = get_song_urls(artist_name)
    for url in urls:
        lyrics = scrape_lyrics(url)
        f.write(lyrics)
    f.close()


class InputBox(BoxLayout):
    def visualize_lyrics_data(self, artist_name):
        write_lyrics_to_file(artist_name)
        f = open(f'{artist_name.lower()}.txt', 'r+', encoding='utf-8')

        # Creates a dict with the lyrics and # of  occurrences
        lyric_frequency = {}
        for lyric in f.read().split():
            if lyric in lyric_frequency:
                lyric_frequency[lyric] += 1
            else:
                lyric_frequency[lyric] = 1

        # List of nouns
        nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}

        # Sorts lyrics by frequency
        asc_lyric_frequency = sorted(lyric_frequency.items(), key=lambda x: x[-1], reverse=True)
        desc_lyric_frequency = sorted(lyric_frequency.items(), key=lambda x: x[-1], reverse=False)

        most_common_lyrics = [value[0] for value in asc_lyric_frequency[:14]]
        most_common_occurrences = [value[1] for value in asc_lyric_frequency[:14]]

        least_common_lyrics = [value[0] for value in desc_lyric_frequency[:14]]
        least_common_occurrences = [value[1] for value in desc_lyric_frequency[:14]]

        most_common_nouns = []
        most_common_nouns_occurrences = []

        # Checks if lyrics are nouns and puts them in most_common_nouns
        while True:
            print(len(most_common_nouns))
            for value in asc_lyric_frequency:
                if value[0] in nouns:
                    most_common_nouns.append(value[0])
                if len(most_common_nouns) == 15:
                    break
            break

        # Appends the corresponding frequency of said nouns to most_common_noun_occurrences
        while True:
            print(len(most_common_nouns_occurrences))
            for value in asc_lyric_frequency:
                if value[0] in most_common_nouns:
                    most_common_nouns_occurrences.append(value[1])
                if len(most_common_nouns_occurrences) == 20:
                    break
            break

        # Creates a 2x2 grid of graphs and plots them
        figure, axis = plt.subplots(2, 2)
        axis[0, 0].bar(most_common_lyrics, most_common_occurrences)
        axis[0, 0].set_title("Most Common Lyrics")

        axis[1, 0].bar(least_common_lyrics, least_common_occurrences)
        axis[1, 0].set_title("Least Common Lyrics")

        axis[0, 1].bar(most_common_nouns, most_common_nouns_occurrences)
        axis[0, 1].set_title("Most Common Nouns")

        plt.show()


class LyricsScraper(App):
    def build(self):
        return InputBox()


if __name__ == '__main__':
    LyricsScraper().run()
