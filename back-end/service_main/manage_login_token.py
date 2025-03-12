import json
from datetime import datetime
from spotifyApi.spotify_auth import get_access_token, get_authorization_code


def manage_login_token():
    """
    Manages the login token by checking if it exists and is valid.
    If the token doesn't exist or has expired, it gets a new one.
    Returns the access token.
    """
    try:
        # Try to open the existing login.json file
        with open('login.json', 'r', encoding='utf-8') as file:
            login_data = json.load(file)
            print("Se encontro el archivo login.json")

            # Check if token is older than 1 hour
            create_time = datetime.strptime(
                login_data["create_time"], "%Y-%m-%d %H:%M:%S.%f")
            if (datetime.now() - create_time).seconds > 3600:
                # Get new authorization code
                authorization_code = get_authorization_code()
                if not authorization_code:
                    print("No se pudo obtener el código de autorización.")
                    return None

                # Get new access token
                access_token, refresh_token = get_access_token(
                    authorization_code)
                if access_token is None:
                    print("No se pudo obtener el token de acceso.")
                    return None

                # Update token information
                login_data["create_time"] = str(datetime.now())
                login_data["access_token"] = access_token

                # Save updated information to file - this was missing
                with open('login.json', 'w', encoding='utf-8') as write_file:
                    json.dump(login_data, write_file)

            return login_data["access_token"]

    except FileNotFoundError:
        # Create new login.json file
        login_data = {
            "create_time": "",
            "access_token": ""
        }

        with open('login.json', 'w', encoding='utf-8') as file:
            json.dump(login_data, file)
            print("Se creo el archivo login.json")

        # Get new authorization code
        authorization_code = get_authorization_code()
        if not authorization_code:
            print("No se pudo obtener el código de autorización.")
            return None

        # Get new access token
        access_token, refresh_token = get_access_token(authorization_code)
        if access_token is None:
            print("No se pudo obtener el token de acceso.")
            return None

        # Update token information
        login_data["create_time"] = str(datetime.now())
        login_data["access_token"] = access_token

        # Save updated information to file - this was missing
        with open('login.json', 'w', encoding='utf-8') as write_file:
            json.dump(login_data, write_file)

        return access_token
