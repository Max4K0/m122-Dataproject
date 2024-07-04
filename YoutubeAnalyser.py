import requests
import pandas as pd
import json
import os




BASE_URL = 'https://youtube138.p.rapidapi.com/video/details/'
settings = {}
# Auslesen funktionen
# Standard-Konfigurationsdatei
def create_default_config(config_file):
    default_config = {
        "Downloadart": "zip",
        "Modus": "None",
        "API Key": "",
        "Youtube Links": [],
        "Downloadpfad": "",
        "Zahl": 5,
        "Boolean": true
    }
    with open(config_file, 'w') as file:
        json.dump(default_config, file, indent=4)
    print(f"Standard-Konfigurationsdatei {config_file} wurde erstellt.")


#Einlesen der Konfigurationsdatei und Validierung der Einstellungen
def load_config(config_file):
    if not os.path.exists(config_file):
        create_default_config(config_file)
        raise FileNotFoundError(f"Die Konfigurationsdatei {config_file} existierte nicht und wurde erstellt. Bitte füllen Sie die Datei aus.")

    with open(config_file, 'r') as file:
        config = json.load(file)



    # Downloadart validieren
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

    # API Key validieren
    api_key = config.get('API Key')
    if api_key:
        settings['API Key'] = api_key
    else:
        raise ValueError("Fehlerhafte Configfile: API Key darf nicht leer sein.")

    # YouTube Links validieren
    youtube_links = config.get('Youtube Links')
    for ylink in youtube_links:
        ylink.replace("https://www.youtube.com/watch?v=", "")

    if youtube_links and isinstance(youtube_links, list) and all(isinstance(link, str) for link in youtube_links):
        settings['Youtube Links'] = youtube_links

    else:
        raise ValueError("Fehlerhafte Configfile: Youtube Links darf nicht leer sein und muss eine Liste von Strings sein.")

    # Downloadpfad validieren
    download_path = config.get('Downloadpfad', '')
    if not download_path:
        download_path = os.getcwd()
    settings['Downloadpfad'] = download_path

    # Zahl von 1-10 einlesen
    number = config.get('Zahl')
    if isinstance(number, int) and 1 <= number <= 10:
        settings['Zahl'] = number
    else:
        raise ValueError("Fehlerhafte Configfile: Zahl muss eine Zahl zwischen 1 und 10 sein.")

    # Boolean einlesen
    boolean_value = config.get('Boolean')
    if isinstance(boolean_value, bool):
        settings['Boolean'] = boolean_value
    else:
        raise ValueError("Fehlerhafte Configfile: Boolean muss ein boolescher Wert sein.")

    return settings

# API
# Funktion zum Abrufen von Videodetails
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


# compare and filter
# Funktion zum Vergleichen und Sortieren der Arrays
def compare_and_sort(arrays, output_count):
    comparisons = []

    # Vergleich der Arrays (nur die ersten drei Arrays werden verglichen)
    for i in range(len(arrays[0])):
        max_value = max(arrays[0][i], arrays[1][i], arrays[2][i])
        comparisons.append(max_value)

    # Absteigend sortieren
    comparisons.sort(reverse=True)

    # Begrenzen der Ausgabe auf die gewünschten Anzahl der größten Zahlen
    return comparisons[:output_count]


# Funktion zum Schreiben der Arrays in eine .txt-Datei
def write_arrays_to_file(arrays, filename):
    with open(filename, 'w') as file:
        for array in arrays:
            file.write(' '.join(map(str, array)) + '\n\n')
    print(f"Arrays wurden in '{filename}' geschrieben.")


# Funktion zum Filtern und Schreiben der Arrays basierend auf Booleans
def filter_and_write_arrays(arrays, booleans, filename):
    with open(filename, 'w') as file:
        for array, boolean in zip(arrays, booleans):
            if boolean:
                file.write(' '.join(map(str, array)) + '\n\n')
    print(f"Gefilterte Arrays wurden in '{filename}' geschrieben.")




















# Main
if __name__ == "__main__":
    config_file_path = 'config.json'
    try:
        settings = load_config(config_file_path)
        print("Einstellungen erfolgreich geladen:", settings)
        videolist = settings['Youtube Links']
        video_id = videolist[0]
        video_details = get_video_details(video_id)
        if video_details:
            df = pd.DataFrame([video_details])
            print(df)
            df.to_csv('video_details.csv', index=False)

        #for arrays in settings['Youtube Links']:
        #   array1 = video_info






        #for link in settings['Youtube Links']:
        #   arrays = arrays.append(get_video_details(link))
        #array1 = get_video_details()
        array1 = [15, 25, 35]
        array2 = [15, 25, 35]
        array3 = [5, 50, 40]
        array4 = [10, 20, 30]
        array5 = [10, 20, 30]

        # Booleans für den Filtermodus
        a = True
        b = False
        c = True
        d = True
        e = False

        # Variable für die Anzahl der auszugebenden größten Zahlen
        output_count = 2



        # Hauptlogik basierend auf dem Modus
        arrays = [array1, array2, array3, array4, array5]
        booleans = [a, b, c, d, e]

        if settings['Modus'] == "Compare":
            result = compare_and_sort(arrays, output_count)
            write_arrays_to_file(arrays, 'output_compare.txt')
        elif settings['Modus'] == "None":
            write_arrays_to_file(arrays, 'output_none.txt')
        elif settings['Modus'] == "Filter":
            filter_and_write_arrays(arrays, booleans, 'output_filter.txt')
        elif settings['Modus'] == "Both":
            result = compare_and_sort(arrays, output_count)
            print("Ergebnis der Vergleiche:", result)
            filter_and_write_arrays(arrays, booleans, 'output_both.txt')
        else:
            print(f"Der Modus {settings['Modus']} wird derzeit nicht unterstützt.")


    except Exception as e:
        print(e)


