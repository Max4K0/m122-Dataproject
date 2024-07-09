# Made by Max | Modul: m164 | Juni/Juli 2024 | alle Rechte vorbehalten

import requests
import pandas as pd
import json
import os


BASE_URL = 'https://youtube138.p.rapidapi.com/video/details/'
settings = {}


# Auslesen funktionen
# Standard Konfigurationsdatei
def create_default_config(config_file):
    default_config = {
        "Downloadart": "zip",
        "Modus": "None",
        "API Key": "",
        "Youtube Links": [],
        "Downloadpfad": "",
        "Filter": {
            "title": True,
            "length": True,
            "publishedDate": True,
            "viewCount": True,
            "likeCount": True,
            "url": True,
            "description": True

        }
    }
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Konfigurationsdatei wurde erstellt.")


#Einlesen der Konfigurationsdatei und Überprüfung der Einstellungen
def load_config(config_file):
    if not os.path.exists(config_file):
        create_default_config(config_file)
        raise FileNotFoundError(
            f"Die Konfigurationsdatei {config_file} existierte nicht und wurde erstellt. Bitte füllen Sie die Datei aus.")

    with open(config_file, 'r') as file:
        config = json.load(file)

    # Downloadart
    valid_download_types = ['tar', 'zip', 'txt']
    download_type = config.get('Downloadart')
    if download_type in valid_download_types:
        settings['Downloadart'] = download_type
    else:
        raise ValueError("Fehlerhafte Configfile: Downloadart ist ungültig.")

    # Modus kann "Compare", "Filter", "Both" oder "None" sein
    valid_mode_types = ['Compare', 'Filter', 'Both', "None"]
    mode_type = config.get('Modus')
    if mode_type in valid_mode_types:
        settings['Modus'] = mode_type
    else:
        raise ValueError("Fehlerhafte Configfile: Modus ist ungültig.")

    # API Key
    api_key = config.get('API Key')
    if api_key:
        settings['API Key'] = api_key
    else:
        raise ValueError("Fehlerhafte Configfile: API Key darf nicht leer sein.")

    # YouTube Links
    youtube_links = config.get('Youtube Links')
    if youtube_links and isinstance(youtube_links, list) and all(isinstance(link, str) for link in youtube_links):
        settings['Youtube Links'] = [link.replace("https://www.youtube.com/watch?v=", "") for link in youtube_links]
    else:
        raise ValueError("Fehlerhafte Configfile: Youtube Links darf nicht leer sein.")

    # Downloadpfad
    download_path = config.get('Downloadpfad', '')
    if not download_path:
        download_path = os.getcwd()
    settings['Downloadpfad'] = download_path

    # Filter einlesen
    filter_settings = config.get('Filter', {})
    settings['Filter'] = {
        'title': filter_settings.get('title', True),
        'url': filter_settings.get('url', True),
        'length': filter_settings.get('length', True),
        'description': filter_settings.get('description', True),
        'publishedDate': filter_settings.get('publishedDate', True),
        'viewCount': filter_settings.get('viewCount', True),
        'likeCount': filter_settings.get('likeCount', True)

    }
    return settings


#API
#Funktion zum Abrufen von Videodetails
def get_video_details(video_id):
    headers = {
        'X-RapidAPI-Host': 'youtube138.p.rapidapi.com',
        'X-RapidAPI-Key': settings['API Key']
    }
    params = {
        'id': video_id
    }
    response = requests.get(BASE_URL, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        video_info = {
            'title': data.get('title'),
            'length (sek)': data.get('lengthSeconds'),
            'publishedDate': data.get('publishedDate'),
            'viewCount': data.get('stats', {}).get('views'),
            'likeCount': data.get('stats', {}).get('likes'),
            'url': f"https://www.youtube.com/watch?v={video_id}",
            'description': data.get('description'),

        }
        return video_info
    else:
        print(f"Fehler: {response.status_code}")
        return None


#compare and filter
#Funktion zum Vergleichen und Sortieren der Arrays
def compare_and_sort(data):
    compare = pd.concat(data)
    compare2 = compare.max()
    return compare2.to_dict()


#Funktion zum Filtern oder ausgeben
def filter_and_write_data(data, filter_settings, filename):
    with open(filename, 'a') as file:
        for key, value in data.items():
            if filter_settings.get(key, True) or settings['Modus'] != "Filter" and settings['Modus'] != "Both":
                file.write(f"{key}: {value}\n")
        file.write(f"-----------------------\n\n")


#Main
if __name__ == "__main__":


    config_path = 'config.json'
    try:
        settings = load_config(config_path)
        print("Einstellungen erfolgreich geladen:", settings)

        all_video_details = []

        for video_id in settings['Youtube Links']:
            video_details = get_video_details(video_id)
            if video_details:
                all_video_details.append(video_details)

        if not all_video_details:
            raise ValueError("Fehlerhafte Videolinks oder das Limit vom API Key ist erreicht.")

        csv = pd.DataFrame(all_video_details)
        csv.to_csv(os.path.join(settings['Downloadpfad'], 'output.csv'), index=False)

        #Modus
        if settings['Modus'] == "Compare":
            result = compare_and_sort([csv])
            filter_and_write_data(result, settings['Filter'],'output.txt')

        elif settings['Modus'] == "None" or settings['Modus'] == "Filter":
            for video in all_video_details:
                filter_and_write_data(video, settings['Filter'], 'output.txt')


        elif settings['Modus'] == "Both":
            for video in all_video_details:
                filter_and_write_data(video, settings['Filter'], 'output.txt')

        else:
            print(f"Der Modus {settings['Modus']} wird derzeit nicht unterstützt.")



    except Exception as e:
        print(e)


