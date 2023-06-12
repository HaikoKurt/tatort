# tatort

## Zielsetzung
Skript bzw. Service zum automatischen Benennen von Tatortfolgen für PLEX Media-Server. Das Skript holt sich die Tatort Folgen von https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen und legt eine Liste mit absoluten Episodennummern und Titel an. Tatortfolgen, die mit MediathekView geladen wurden und sich im Quellverzeichnis `SOURCE_DIR` befinden werden mit der Titelliste abgeglichen und entsprechend umbenannt*) und in das Zielverzeichnis `DEST_DIR` verschoben. Das Skript verschiebt alle Dateien, unabhängig von der Dateiendung, damit auch Filmbeschreibungen und Untertiteldateien entsprechend benannt werden. Die Dateien werden im Zielverzeichnis jahrgangsweise abgelegt. Dubletten werden in das Verzeichnis `DUPLICATE_DIR` verschoben.

*) Schema: {ziel}/{jahr}/Tatort - (S{jahr}_E{folge}) - {titel}{ext}

```
1970/Tatort - (S1970_E02) - Saarbrücken an einem Montag.mp4
```

## Realisierungsvarianten
### Skript manuell ausführen
Dazu wird das Python Skript `tatort_file_map.py` entsprechend angepasst (Quell- und Zielverzeichnisse) und manuell gestartet.

### Docker-Service mit Watchfolder
Die Backend-(renamer)-Komponente wird in Docker installiert und entsprechend angepasst (Quell- und Zielverzeichnis). Nach dem Starten wird das Quelverzeichnis (`SOURCE_DIR` bzw. `/source`-Volume) überwacht und falls dort eine Datei landet, die den Kriterien entspricht, wird sie verschoben. Dabei wird so, lange gewartet, bis die Datei nicht mehr wächst.
1. Systemdateien werden ignoriert (Dateiennamen, die mit '.' beginnen)
1. Dateien mit Namen, die nicht mit 'Tatort' beginnen, werden nach `SOURCE_DIR/unknown` verschoben
1. Dateien mit Namen, in denen kein Episodentitel gefunden wird, werden nach `SOURCE_DIR/unknown` verschoben
1. Dateien mit Namen, die im Zielverzeichnis bereits existieren, werden nach `SOURCE_DIR/duplicate` verschoben
1. Alle anderen Dateien werden ins Zielverzeichnis `DEST_DIR` verschoben.

Die Protokoll-Datei liegt im Ordner `SOURCE_DIR/logs`.

***Anmerkung:** Zur Überwachung des Quellverzeichnisses wurde auf die Verwednung der Python Bibliothek `watchdog` verzichtet, wiel diese auf meinem NAS zu Fehlverhalten führte. Das Eigenbau-Modul `watchfolder` läuft auf meinem QNAP-NAS problemlos, verhält sich aber im Docker-Container auf dem Mac nicht immer korrekt (Dateien werden verschoben, obwohl der Kopiervorgang noch nicht abgeschlossen wurde). Ich freue mich über Vrebesserungsvorschläge!*
## Bekannte Probleme
1. Es gibt Tatortfolgen mit identischen Titeln (neun Paare). Es wird immer die niedrigste Folgennummer zugeordnet. Das ist in 50% der Fälle falsch.
1. Das Skript wurde mit 250 Folgen getestet. Probleme machen insbesondere Umlaute, Satzzeichen und Groß-/Kleinschreibung, die durch eine Normalisierung gelöst werden. Möglicherweise gibt es Zeichen, die das Skript noch nicht korrekt normalisiert.
1. Kurze Titel können Teile von langen Titeln sein (Bsp: 'Väter' in 'Söhne und Väter'). Aus diesem Grund werden die längsten Titel zuerst verglichen. Dadurch, dass es sehr kurze Titel gibt, kann es zu Fehlzuordnungen kommen, wenn wegen falscher Normalisierung, der lange Titel nicht trifft (Bsp: 'KI' in 'Schimanskis Waffe').

Das bedeutet, dass nach einer Umbenennung immer noch einmal manuell kontrolliert werden sollte. Das ist leider nicht perfekt, aber trotzdem hilft das Skript sehr viel manuelle Arbeit zu vermeiden.

## Mögliche Erweiterungen

1. Zusätzliche Informationen aus dem Dateinamen verwenden um die Zuordnung zu verbessern.
1. Informationen aus dem Docker-Backend in eine Datenbank schreiben und in einem Docker-Web-Frontend anzeigen.
1. Konfigurationsmöglichkeiten über das Docker Frontend anbieten (z.B. die Tabelle mit den Tatort-Reihennummern (`SEASONS` in `Renamer`), welche jedes Jahr ergänzt werden muss.) oder die Tabelle automatisch aus den Informationen auf Wikipedia erzeugen (geht das?)
1. In der Episodentabelle die doppelten Titel gänzlich entfernen, sodass Tatorte mit den Zwillingstiteln nach Unbekannt (`unknown`) verschoben werden (Bekanntes Problem 1).
1. Falls eine Folge geladen wird und diese bereits existiert, prüfen, ob die Mediendatei größer ist (bessere Qualität) und dann ersetzen.

## Auf NAS installieren (Backend)

1. Image bauen `docker build . -t tatort.renamer:<version>` in den Unterverzeichnissen
1. TAR-File von den Images erzeugen `docker save -o tatort.renamer-<version>.tar tatort.renamer`
1. TAR-File auf NAS kopieren und importieren \
Dabei `/source`- und `/destination`-Volumes entsprechend anpassen.