import requests
import pandas as pd


RAPIDAPI_KEY = 'aa918de1fbmsh5b2652825114a1ep16553ejsn1007eaeace78'
BASE_URL = 'https://youtube138.p.rapidapi.com/video/details/'

# Funktion zum Abrufen von Videodetails
def get_video_details(video_id):
    url = BASE_URL
    headers = {
        'X-RapidAPI-Host': 'youtube138.p.rapidapi.com',
        'X-RapidAPI-Key': RAPIDAPI_KEY
    }
    params = {
        'id': video_id
    }
    response = requests.get(url, headers=headers, params=params)
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

# Beispiel Video-ID (ersetze dies durch eine echte Video-ID)
video_id = 'lyTQPTLYOw4'
video_details = get_video_details(video_id)

# Ausgabe der Video-Details
if video_details:
    df = pd.DataFrame([video_details])
    print(df)

    # Optional: Daten als CSV speichern
    df.to_csv('video_details.csv', index=False)
