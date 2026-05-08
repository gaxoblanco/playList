# Lineup → Spotify Playlist

You're at a festival. You see the poster. You want the playlist.

Take a photo of the festival banner → the app reads the band names with OCR → 
creates a Spotify playlist with their top tracks. Done.

Built during a trip to The Hague in 2024.

## How it works

1. **OCR** — extracts band names from the festival image
2. **Spotify API** — finds each band and grabs their top 5 tracks  
3. **Playlist** — creates and populates it automatically in your Spotify account

## Stack

Python · OCR · Spotify API · Docker

## Run it

```bash
cd festivalMusic
git pull
docker-compose restart
```
