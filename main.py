from bs4 import BeautifulSoup
import requests
import time
import matplotlib.pyplot as plt

all_lyrics = ''

song_urls = []	
html_azlyrics = requests.get("https://www.azlyrics.com/c/clairo.html").text
soup = BeautifulSoup(html_azlyrics, 'html.parser')
songs = soup.find_all('div', class_='listalbum-item')
for div in songs:
    for a in div.find_all('a'):
        song_urls.append((a['href'][3:]))

for url in song_urls:
	if url[0] == 'l':
	    html_song = requests.get(f"https://www.azlyrics.com/{url}").text
	    soup_2 = BeautifulSoup(html_song, 'html.parser')
	    lyrics = soup_2.find_all('div')[11]
	    print(url)
	    for lyric in (lyrics.find_all('div')[8].get_text().encode('ascii', 'ignore').decode()):
	    	all_lyrics += lyric
	    time.sleep(3)
	else:
		pass

word_frequency = {}

for word in all_lyrics.replace("'", '').replace("?", '').replace('!', '').replace('!', '').replace('"', '').split():
    if word in word_frequency:
        word_frequency[word] += 1
    else:
        word_frequency[word] = 1

sort_word_frequency = sorted(word_frequency.items(), key=lambda x: x[-1], reverse=True)
print(sort_word_frequency)

lyrics_plot = plt.bar([value[0] for value in sort_word_frequency[:9]], [value[1] for value in sort_word_frequency[:9]])
plt.xlabel('Lyrics')
plt.ylabel('# of Occurrences')
plt.show()

