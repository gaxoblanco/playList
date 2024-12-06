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

--------------------------------
# Tutorial for Playlist path
**Upload the image:

    Crop an image containing the list of festival bands beforehand.
    Upload the image in the designated section of the app. Ensure the text is clear and legible.

**Review suggested names:

    The software will analyze the image and generate a list of potential band names.
    You'll enter an interactive "game" where you can select, correct, or delete names as needed. This is important because recognition may not be perfect.

**Confirm and adjust the list:

    After finishing the process, review the final list of bands that will perform at the festival.
    Make final adjustments: correct names, remove bands that don't belong, or delete ones you don’t want to include.

**Create the playlist:

    Enter a name for the playlist in the input field.
    Click the "Create" button. The software will process the list and add the top 10 most popular songs of each band.

**Finish and contribute:

    You’ll receive a summary of the process, along with links to access your playlist.
    If you’d like to support the project, you can use the available donation buttons.

------
# Formato de los Obj
** associated_data
associated_data = {'name': 'tex in img', 'band_id': 'id by platform', 'img_zone': [X, Y, W, H]}

** text_zone
text_zone = {'text': 'tex in img', 'position': (X, Y, W, H)}