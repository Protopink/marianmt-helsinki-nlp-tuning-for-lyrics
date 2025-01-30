import requests
from bs4 import BeautifulSoup
import time

base_url = "https://lyricstranslate.com"

def get_song_links(artist_url):
    print("Fetching poular songs for `", artist_url, "`")

    response = requests.get(artist_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for row in soup.find_all("td", class_="songName"):
        link = row.find("a", href=True)
        if "/en/" in link["href"]:  # Ensure it leads to English lyrics
            links.append(link["href"])

    return links

def scrape_lyrics(song_url):
    song_full_url = base_url + song_url

    print("Scraping lyrics from `" + song_full_url + "`")

    # TODO: make sline splitting right with repsect to `div.par > .ll-X-Y`

    response = requests.get(song_full_url)
    soup = BeautifulSoup(response.text, "html.parser")
    original_lyrics = [x for x in soup.find("div", { "id": "song-body" }).get_text("\n", strip=True).split("\n") if x]
    russian_translation_urls = []

    for element in soup.find_all("div", class_="slist"):
        if "Russian" in element.get_text():
            for link in element.find_all("a", href=True):
                russian_translation_urls.append(link["href"])
            break

    if len(russian_translation_urls) == 0:
        return original_lyrics, []
    
    print("Found", len(russian_translation_urls), "Russian translations for", song_full_url, ":", russian_translation_urls)

    translations = []
    
    for translation_url in russian_translation_urls:
        song_translation_url = base_url + translation_url

        print("Scraping lyrics translation from `" + song_translation_url + "`")

        response = requests.get(song_translation_url)
        soup = BeautifulSoup(response.text, "html.parser")
        translated_lyrics = [x for x in soup.find("div", { "id": "song-body" }).get_text("\n", strip=True).split("\n") if x]

        translations.append(translated_lyrics)

        time.sleep(3) # Be polite to the server

    return original_lyrics, translations


artist_urls = ["https://lyricstranslate.com/en/muse-lyrics.html"]
scraped_urls = []
songs_written = 0
lines_written = 0

with open("tuning/source.txt", "w", encoding="utf-8") as src, open("tuning/target.txt", "w", encoding="utf-8") as dest:
    for artist_url in artist_urls:
        song_links = get_song_links(artist_url)

        print("Found", len(song_links), "songs for translation for `", artist_url)

        for song in song_links:
            if song in scraped_urls:
                print("SKIPPING", song, "cause it is already scraped")
                continue

            original_lyrics, translations = scrape_lyrics(song)
            original_len = len(original_lyrics)

            if len(translations) == 0:
                continue

            for i in range(1, len(translations)):
                if original_len != len(translations[i]):
                    continue

                src.write("\n".join(original_lyrics) + "\n")
                dest.write("\n".join(translations[i]) + "\n")

                lines_written += original_len

            scraped_urls.append(song)
            songs_written += 1

            if songs_written % 10 == 0:
                print("Scraped", songs_written, "of", len(song_links), "songs with", lines_written, "lines of lyrics!")
                time.sleep(5) # Be polite to the server
            
            time.sleep(len(translations) * 1.5) # Be polite to the server

print("Scraped", songs_written, "songs with", lines_written, "lines of lyrics!")
