=========================================
Project: Spotify Playlist from Festival Banner
=========================================

Overview:
---------
This project automatically creates a Spotify playlist from an image of a festival banner, which displays the names of the bands attending the event. The process is divided into several stages, each handled by different scripts.

Steps:
------

1. **Extract Band Names from Banner (img_process.py)**:
   - A machine learning model processes the banner image and extracts the band names, generating a JSON file with the following format:
     ```
     [
       {
         "name": "OLIVIA RODRIGO"
       }
     ]
     ```

2. **Retrieve Band IDs (process_list_band_id.py)**:
   - This script takes the previous JSON and uses the Spotify API to obtain the unique `band_id` for each band.

3. **Fetch Top Tracks (process_list_band_top.py)**:
   - Using the band IDs, the script retrieves the top 5 tracks for each band. The output JSON looks like this:
     ```
     {
       "name": "LA CINTIA",
       "band_id": "3NIZFmehJM8YiGpCdihlck",
       "top_tracks": [
         {
           "name": "Vivir Lo Nuestro",
           "uri": "spotify:track:4qAknKWl2aMvWn4r1nzWAa"
         },
         ...
       ]
     }
     ```

4. **Interact with Spotify API (spotify_api.py)**:
   - This script contains functions to interact with Spotify's API, including creating a new playlist. It generates a JSON with key playlist details:
     ```
     {
       "href": "https://open.spotify.com/playlist/63tEphBsbZ2usOOrEqEmEg",
       "id": "63tEphBsbZ2usOOrEqEmEg",
       "images": [],
       "name": "lola2025"
     }
     ```

5. **Add Tracks to Playlist (process_list_band_add_to_playlist.py)**:
   - This final script adds each song to the playlist using its unique `uri` provided by Spotify.

Result:
-------
A Spotify playlist is automatically generated, featuring the most popular songs of the bands attending the festival.

