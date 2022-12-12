# Afra An-und Abmeldung - Code
## Extension
Da es einen Fehler in NGINX Unit gibt, durch welchen WebSocket-Verbindungen von Firefox mit meinem Server nicht funktionieren, musste ich eine Browser-Extension schreiben, welche den Fehlergrund beseitigt, bis der Fehler gepatched wird. Genaueres dazu hier: https://github.com/nginx/unit/issues/772

## Server
Im Ordner befinden sich die für die Funktion wesentlichen Dateien des Servers. Einzelne Dateien, welche ebenfalls für den Server wichtig sind, jedoch nicht preisgegeben werden sollen, wie Private-Keys sind aus Sicherheitsgründen nicht enthalten. 
Auch wurden Passwörter und derartige Sicherheitsrisiken im Code unkenntlich gemacht.

Die CSV-Datei, mit welcher die Datenbank gefüllt wird, wurde geleert und mit einem Test-Datensatz gefüllt. Dies geschah zum Schutz der Schülerdaten. Aus demselben Grund ist auch die Datenbank nicht enthalten. Diese kann jedoch mit den entsprechenden Befehlen neu aufgesetzt werden. Hierbei entsteht eine neue, leere Datenbank, an welcher man jedoch die Struktur erkennen kann. Siehe hier: https://docs.djangoproject.com/en/4.1/ref/django-admin/#migrate
