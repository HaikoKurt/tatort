# tatort

## Zielsetzung
Skript zum automatischen Benennen von Tatortfolgen für PLEX Media-Server. Das Skript holt sich die Tatort Folgen von https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen und legt eine Liste mit absoluten Episodennummern und Titel an. Tatortfolgen, die mit MediathekView geladen wurden und sich im Quellverzeichnis `SOURCE_DIR` befinden werden mit der Titelliste abgeglichen und entsprechend umbenannt*) und in das Zielverzeichnis `DEST_DIR` verschoben. Das Skript verschibt alle Dateien, unabhängig von der Dateiendung, damit auch Filmbeschreibungen und Untertiteldateien entsprechend benannt werden. Die Dateien werden im Zielverzeichnis jahrgangsweise abgelegt. Dubletten werden in das Verzeichnis `DUPLICATE_DIR` verschoben.

*) Schema: {ziel}/{jahr}/Tatort - (S{jahr}_E{folge}) - {titel}{ext}

```
1970/Tatort - (S1970_E02) - Saarbrücken, an einem Montag.mp4
```

## Bekannte Probleme
- Es gibt Tatortfolgen mit identischen Titeln (neun Paare). Es wird immer die niedrigste Folgennummer zugeordnet. Das ist in 50% der Fälle falsch.
- Das Skript wurde mit 250 Folgen getestet. Probleme machen insbesondere Umlaute, Satzzeichen und Groß-/Kleinschreibung, die durch eine Normalisierung versucht wird zu lösen. Möglicherweise gibt es Zeichen, die das Skript noch nicht korrekt normalisiert.
- Kurze Titel können Teile von langen Titeln sein (Bsp: 'Väter' in 'Söhne und Väter'). Aus diesem Grund werden die längsten Titel zuerst verglichen. Dadurch, dass es sehr kurze Titel gibt, kann es zu Fehlzuordnungen kommen, wenn wegen falscher Normalisierung, der lange Titel nicht trifft (Bsp: 'KI' in 'Schimanskis Waffe').

Das bedeutet, dass nach einer Umbenennung immer noch einmal manuell kontrolliert werden sollte. Das ist leider nicht perfekt, aber trotzdem hiflt das Skript sehr viel manuelle Arbeit zu vermeiden.

## Mögliche Erweiterungen

- Als Prozess in einem Docker-Container auf dem NAS laufen lassen, um einen Watchfolder zu überwachen und die Dateien automatisch umzubenennen und in den PLEX-Medienordner zu schieben.
- Zusätzliche Informationen aus dem Dateinamen verwenden um die Zuordnung zu verbessern.