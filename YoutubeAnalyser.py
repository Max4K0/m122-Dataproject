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
            "publishedDate": True,
            "viewCount": True,
            "likeCount": True,
            "commentCount": True
        }
    }
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Standard Konfigurationsdatei {config_file} wurde erstellt.")


#Einlesen der Konfigurationsdatei und Überprüfung der Einstellungen
def load_config(config_file):
    if not os.path.exists(config_file):
        create_default_config(config_file)
        raise FileNotFoundError(f"Die Konfigurationsdatei {config_file} existierte nicht und wurde erstellt. Bitte füllen Sie die Datei aus.")

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
        'publishedDate': filter_settings.get('publishedDate', True),
        'viewCount': filter_settings.get('viewCount', True),
        'likeCount': filter_settings.get('likeCount', True),
        'commentCount': filter_settings.get('commentCount', True)
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
            'publishedDate': data.get('publishedDate'),
            'viewCount': data.get('viewCount'),
            'likeCount': data.get('likeCount'),
            'commentCount': data.get('commentCount')
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

#Funktion zum Schreiben der Arrays in eine .txt
def write_arrays_to_file(data, filename):
    with open(filename, 'w') as file:
        for key, value in data.items():
            file.write(f"{key}: {value}\n")
    print(f"Arrays wurden in '{filename}' geschrieben.")

#Funktion zum Filtern
def filter_and_write_data(data, filter_settings, filename):
    with open(filename, 'w') as file:
        for key, value in data.items():
            if filter_settings.get(key, True):
                file.write(f"{key}: {value}\n")
    print(f"Gefilterte Daten wurden in '{filename}' geschrieben.")




















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
            raise ValueError("Es gibt keine Videodetails.")

        csv = pd.DataFrame(all_video_details)
        csv.to_csv(os.path.join(settings['Downloadpfad'], 'output.csv'), index=False)

        if settings['Modus'] == "Compare":
            result = compare_and_sort([csv])
            write_arrays_to_file(result, 'output.txt')
        elif settings['Modus'] == "None":
            write_arrays_to_file(all_video_details, 'output.txt')

        elif settings['Modus'] == "Filter":
            for video in all_video_details:
                filter_and_write_data(video, settings['Filter'], 'output.txt')
        elif settings['Modus'] == "Both":
            for video in all_video_details:
                filter_and_write_data(video, settings['Filter'], 'output.txt')

        else:
            print(f"Der Modus {settings['Modus']} wird derzeit nicht unterstützt.")






        #for link in settings['Youtube Links']:
        #   arrays = arrays.append(get_video_details(link))
        #array1 = get_video_details()




    except Exception as e:
        print(e)


