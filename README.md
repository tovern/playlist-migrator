# Playlist Migrator

## Overview

Allows liked songs / favourite tracks / playlists to be exported from one streaming music provider and imported into another.

## Usage

```bash
main.py [-h] {spotify,youtube} {import,export}
```

## Provider Integration

### YTMusic

Simply run:
```bash
ytmusicapi oauth
```
and follow the instructions. This will create a file oauth.json in the current directory.

### Spotify

Add a new app to the [Spotify API](https://developer.spotify.com/dashboard/). Pay attention to the SPOTIPY_REDIRECT_URI, this does NOT need to be a valid resolvable URI, but it must match the environmental variable that you set later.

Export the following variables:
```bash
export SPOTIPY_CLIENT_ID=XXX
export SPOTIPY_CLIENT_SECRET=XXX
export SPOTIPY_REDIRECT_URI=http://localhost:7777/callback
```

