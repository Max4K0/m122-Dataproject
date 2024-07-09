# Youtube Analyser
<span style="color:darkgray">m122-Dataproject</span>

<span style="color:darkgray">Teilnehmer: Max</span>

----------------

In dem Projekt geht es darum Daten von Youtube videos rauszulesen, zu analysieren und sie zu konvertieren.

Daraus ist es möglich Daten wie views, likes, kommentare, upload und noch vieles mehr zu filtern und zu vergleichen.

Das Projekt wird mit Python begleitet sowie der Youtube APIs.

----------------

### Vorgehen des Systems:
wir wollen mit Remotedaten arbeiten, also werden die Daten auf einen Server geladen verarbeitet und dann wieder ausgegeben.

### Systeme:
Die Umgebung wird mit Intellij, Python und FTP geführt und mit git dokumentiert.
Dazu wird uns ein AWS Amazon Server bereitgestellt.


Folgende Details gibt es zu klären:

### Konfiguration:
Die Konfig file wird in .json geladen. Diese sind auf dem Server gespeichert diese beinhalten daten wie
die Download art (zip, tar, txt), die api keys sowohl die Databases, wo diese gespeichert wurden.

### Get-Prozedur:
Daten von der Youtube api werden erst im programm rein geladen. Die Raw daten werden immer gespeichert in der Database.
Das gleiche gilt für die editierten Daten.

### Weiterreichung:
Das Programm läuft komplett auf dem Server. Man kann über putty oder über Windows die konsole öffnen und das Programm ausführen.

### Sicherheitsaspekte:
Da es hier um rein öffentliche Daten geht, wird keine Sicherheit benötigt.

### Folgende Features müssen implementiert werden:
Funktionalität der Youtube API
Download Möglichkeit der Daten.
Verarbeitung wie Filterung und Speicherfähigkeit der Daten.

### Folgende Features sind Optional einzubinden:
Zip und Tar Fähigkeit beim output.
Schöne TUI Oberfläche beim starten des Programms.

### Systemdesign:

<img width="482" alt="Systemdesign" src="https://github.com/MaxHD00/m122-Dataproject/assets/31143468/8d62bf1f-6e0a-4e3e-b9a0-7ce6029350c6">

### UML Aktivitätsdiagram/Verarbeitung:

<img width="482" alt="Activity-Diagram" src="https://github.com/MaxHD00/m122-Dataproject/assets/31143468/e87d7f03-70f6-4c9e-8b89-4fe88d07dc96">

### Bedienungsanleitung:
Zuerst muss die Lib "Pandas" installiert werden:

"sudo apt install python3-pandas"

Gestartet wird die Python über "python3 YoutubeAnalyser.py"

Nach dem erstausführen erstellt sich eine config.json mit leeren werten.

Diese kann Folgend ausgefüllt werden:

{

"Downloadart": Wie soll die ausgabe gespeichert sein?

"Modus": None,Filter,Compare,Both - Soll gefiltert, verglichen oder nur ausgegeben werden?

"API Key": Hier muss der API Key eingefügt werden.

"Youtube Links": ["link1", "link2",...] - Hier kommen die Youtube Links rein.

"Downloadpfad": Ordner/ - Wo soll die Ausgabe gespeichert werden. (Ordner muss bereits existieren)

"Filter": Welche Inhalte sollen angezeigt werden und welche nicht? Funktioniert nur im Filter und Both Modus.

}

### Projektablauf und Dokumentation interner Funktionen:

Mein Vorgehen war es Anfangs die API nutzen zu können. Dazu suchte ich nach einer geeignetet Youtube API.
Schlussendlich habe ich mich für die Folgende Youtube API auf Rapidapi entschieden:
https://rapidapi.com/Glavier/api/youtube138

Angemeldet und kostenlos abonniert hatte ich anschliessend den API key.

Nun versuchte ich die API erstmal zum Laufen zu bringen. Dazu nahm ich mir die beispiele auf Rapidapi und führte das script aus.

Zugleich versuchte ich alle nötigen Informationen eines Youtube Videos anzeigen zu lassen.

Es freute mich, dass es funktionierte, allerdings konnte ich nicht alle Informationen extrahieren

Mein nächstes Ziel war es fragmente zu erstellen, die immer Teile erfüllen sollen.

-----------------------

Bei mir war das:

API.py->                Greift auf die Python API zu und liesst die Informationen raus.

Auslesen.py->           Kann daten aus einer Json auslesen oder sie auch erstellen.

Compare_and_filter.py   Vergleicht oder Filtert Daten.

Linkcutter.py->         Schneidet den Youtube link aus, da die API meist nur die Video ID aus dem Link benötigt.

-----------------------

Dies alles habe ich dann in die YoutubeAnalyser.py zusammengefasst.

Der Aufbau soll klar strukturiert sein. Oben die Methoden und unten die Main.
Kurz das erklären der Methoden:

create_default_config-> Erstellt eine config.json, sollte sie nicht existieren.

load_config->           Lädt Daten aus der Config und kontrolliert diese auf Richtigkeit.

get_video_details->     Besorgt sich die Videodaten aus der API und speichert sie in das Array "video_info".

compare_and_sort->      Vergleicht Daten untereinander.

filter_and_write_data-> Schreibt die Resultate in die Output File. Wenn Filter/Both aktiv ist, dann filtert die Methode auch.

-----------------------

Nun folgt nur noch die Main, welche alles Lädt und anschliessend in den richtigen Modus wechselt.

### Tests:
Beim Testen sind mir manche Sachen aufgefallen:
- View und likeCount haben keinen output ausgegeben.
- Length funktioniert, aber nach der Zahl hätte ich gerne noch ein "Sekunden" hinzugefügt. Die Info habe ich nun am Anfang hinterlegt.
- VideoID und ganzer Link hatte ab und zu Verwechselungen.
- Compare Modus konnte ich nicht genug testen. Hab den Fokus auf alles andere dann gesetzt.
- Beim Einfügen vom Downloadpfad Setting habe ich das Programm etwas zerstört. Dauerte ein wenig, bis ich den Fehler entdeckt habe.