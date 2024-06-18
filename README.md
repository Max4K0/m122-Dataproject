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

### UML Aktivitätsdiagram/Verarbeitung:

<img width="482" alt="Activity-Diagram" src="https://github.com/MaxHD00/m122-Dataproject/assets/31143468/94f4050c-d5fa-43ce-be29-bcd2951c4a84">

### Systemdesign:

<img width="482" alt="Systemdesign" src="https://github.com/MaxHD00/m122-Dataproject/assets/31143468/f43c7349-6273-4b5d-8a8b-7cf2c2c17ada">

