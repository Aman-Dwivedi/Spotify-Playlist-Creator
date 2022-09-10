"""
Author: Aman Dwivedi
Description: This program creates a Spotify Playlist
for the user according to the billboards top 100 songs of the week. The user
can specify any date to get that particular week's top 100 songs.
01/19/2022 Changes made due to billboard website update and spotify API change.
"""
import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "abd1a71b0084462e9e05fa1c2ce24e7e"
SPOTIFY_CLIENT_SECRET = "2d706b3bb7564fd4b32caebc511138f9"
REDIRECT_URI = "http://example.com"
SCOPE = "playlist-modify-private"


def create_playlist(sp, song_uri, date):
    """
    This function creates the playlist on spotify.
    :param sp: Spotipy object.
    :param song_uri: List of all the song uri on spotify.
    :param date: The input date entered by the user.
    :return: Doesn't return Anything
    """
    user_id = sp.current_user()["id"]
    playlist_id = sp.user_playlist_create(user=user_id, name=f"{date} "
                                                             f"Billboard 100",
                                          public=False,
                                          description="Playlist created using "
                                                      "python of the top 100 "
                                                      "songs on Billboard.")

    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id["id"],
                                tracks=song_uri)


def get_songs_on_spotify(song_list, year):
    """
    This function authenticates user account on spotify, then stores the
    USER_ID and finally creates a list of song uri for the 100 songs listed
    in song_list. If any song is not available on spotify, it prints out a
    prompt in the console.
    :param song_list: python list of 100 song names as strings.
    :param year: string storing the year in which all the songs were
           released. This helps in narrowing down the search on spotify.
    :return: sp is the Spotipy object.
             song_uri is the list of all the song uri on Spotify.
    """
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=REDIRECT_URI, scope=SCOPE))
    song_uri = []
    for song in song_list:
        result = sp.search(q=f"{song} year:{year}", limit=1, type="track")
        if result["tracks"]["items"] == 0:
            print(f"{song} is not available on Spotify.")
        else:

            # try except block added 01/19/2022 Change in spotify API
            try:
                song_uri.append(result["tracks"]["items"][0]["uri"])
            except IndexError:
                print(f"{song.strip()} is not available on Spotify.")
    return sp, song_uri


def main():
    user_input = input("Which year do you want to travel to? Type the date in "
                       "this format YYYY-MM-DD:\n")

    url = "https://www.billboard.com/charts/hot-100/" + user_input

    response = requests.get(url=url)

    # Checks if the URL is correct
    if response.status_code == 404:
        print("Wrong Input. Please start again. The date should be in the "
              "following order: YYYY-MM-DD")
    else:
        song_list = get_song_list(response)
        year = user_input[:4]
        sp, song_uri = get_songs_on_spotify(song_list, year)
        create_playlist(sp, song_uri, date=user_input)
    print("\nPlaylist created enjoy :))")


def get_song_list(response):
    """
    This function scraps the website and creates a list of top 100 songs
    :param response: response received from the website.
    :return: song_list: python list of 100 song names as strings.
    """
    soup = BeautifulSoup(response.text, "html.parser")

    # Generate list of top 100 songs listed on the website
    song_list = [song.getText() for song in soup.select(
        ".c-title.a-no-trucate.a-font-primary-bold-s.u-letter-spacing-0021")]
    return song_list


if __name__ == '__main__':
    main()
