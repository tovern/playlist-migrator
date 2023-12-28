from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os


class Provider:
    """Interacts with a music streaming provider"""
    def __init__(self):
        self.provider = None
        self.tracks = []

    def export_tracks(self):
        """Writes tracks to a JSON file"""
        with open('output.json', 'w') as file:
            file.write(json.dumps(self.tracks))  # use `json.loads` to do the reverse

    def import_tracks(self):
        """Loads tracks from a JSON file"""
        with open('output.json', 'r') as file:
            self.tracks = (json.load(file))

    def spotify_init(self):
        """Initiate connection to Spotify API"""
        scope = "user-library-read user-library-modify playlist-modify-private"
        self.provider = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
        print("sp")

    def spotify_fetch_tracks(self):
        """Gets all tracks from a users 'saved tracks/liked songs' playlist in Spotify"""
        i = 0
        while i < 1000:
            response = self.provider.current_user_saved_tracks(offset=i, limit=20)
            for song in (response["items"]):
                song_dict = {
                    "artist": song["track"]["artists"][0]["name"],
                    "title": song["track"]["name"],
                }
                self.tracks.append(song_dict)
            i += 20
        print(f"Fetched {len(self.tracks)} tracks from Spotify")

    def spotify_add_tracks(self):
        """Adds tracks ta a users 'saved tracks/liked songs' playlist in Spotify"""
        # Find tracks to search for
        for track in self.tracks:
            search_string = f'artist: {track["artist"]},track: {track["title"]}'
            track["searchString"] = search_string
            # Find top matching id for track
            results = self.provider.search(q=search_string, limit=1, type="track", market="GB")
            track["id"] = results["tracks"]["items"][0]["id"]
            # Add to saved tracks playlist
            self.provider.current_user_saved_tracks_add(tracks=[track["id"]])
        print(f"Added {len(self.tracks)} tracks to Spotify playlist")

    def youtube_init(self):
        """Initiate connection to YouTube API"""
        self.provider = YTMusic("oauth.json")
        print("yt")

    def youtube_fetch_tracks(self):
        """Gets all tracks from a users 'Liked Music' playlist in YouTube Music"""
        playlist = self.provider.get_playlist("LM")
        if playlist['trackCount'] > 0:
            for song in playlist['tracks']:
                track = {"artist": song['artists'][0]['name'], "title": song['title']}
                self.tracks.append(track)
            print(f"Fetched {playlist['trackCount']} tracks from YouTube")

    def youtube_add_tracks(self):
        """Adds tracks ta a users 'Liked Music' playlist in YouTube Music"""
        for track in self.tracks:
            # Create a YT friendly search parameter
            search_string = track["artist"] + " " + track["title"]
            track["searchString"] = search_string
            # Search for the top matching track ID
            results = self.provider.search(track["searchString"], "songs")
            track["id"] = results[0]["videoId"]
            # Add to playlist. Replace playlist ID with LM when live
            self.provider.add_playlist_items("VLPLKRob01e0UOV9l-ue_fmoLJK8kGcZikEm", [track["id"]])
        print(f"Added {len(self.tracks)} tracks to YouTube playlist")
