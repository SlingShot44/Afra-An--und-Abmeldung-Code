# Afra An-und Abmeldung - Code
## Extension
Da es einen Fehler in NGINX Unit gibt, durch welchen WebSocket-Verbindungen von Firefox mit meinem Server nicht funktionieren, musste ich eine Browser-Extension schreiben, welche den Fehlergrund beseitigt, bis der Fehler gepatched wird. Genaueres dazu hier: https://github.com/nginx/unit/issues/772

## Server
Im Ordner befinden sich die für die Funktion wesentlichen Dateien des Servers. Die Anwendung ist in mehrere applications unterteilt. Genaueres zur Struktur eines Django-Projekts findet man [hier](https://docs.djangoproject.com/en/4.1/ref/applications/#projects-and-applications) und [hier](https://docs.djangoproject.com/en/4.1/intro/tutorial01/).

### Struktur
#### accounts
Diese appplication kümmert sich um die Verwaltung von Usern (Admin, Mentoren).

#### API
Diese application stellt die API bereit.

#### BackendschluesselKasten
Diese application ist das Zentrum des Servers. Hier liegt die Django-Konfigurations-Datei (settings.py). Weiterhin laufen hier alle Routing-Dateien (urls.py) aber auch die gesamte Anwendung zusammen (asgi.py).

#### WebApp
Diese application stellt die Webanwendung bereit.

#### config
Dieser Ordner enthält weitere wichtige Dateien. 

- "cron.sh" beschreibt einen Cron-Job, welcher einmal im Monat ausgeführt wird
  - Das SSL/TLS-Zertifikat wird erneuert
  - Abgelaufene Sessions werden aus der Datenbank gelöscht
- "houses.json" beinhaltet eine Auskunft über alle möglichen Häuser
- "locations.json" enthält die Liste möglicher Ziele
- "mensarfid.csv" liefert die Schülerdaten, mit welchen die Datenbank gefüllt wird
  - Die Datei wurde geleert und mit einem Test-Datensatz gefüllt. Dies geschah zum Schutz der Schülerdaten.
- "unit.json" entspricht der Konfiguration des NGINX Unit-Servers

#### print
Dieser Ordner war Teil des deaktivierten Druck-Systems. Jetzt beinhaltet er lediglich die PDF, welche der Server generiert, wenn man die Liste herunterlädt.

#### staticfiles
In diesem Ordner befinden sich alle statischen Dateien des Servers gebündelt.

### Datenschutz und Sicherheit
Einzelne Dateien, welche ebenfalls für den Server wichtig sind, jedoch nicht preisgegeben werden sollen, wie Private-Keys sind aus Sicherheitsgründen nicht enthalten. 
Dasselbe gilt für die Datenbank. Diese kann jedoch mit den entsprechenden Befehlen neu aufgesetzt werden (Siehe [hier](https://docs.djangoproject.com/en/4.1/ref/django-admin/#migrate)). Hierbei entsteht eine neue, leere Datenbank, an welcher man jedoch die Struktur erkennen kann. Auch wurden Passwörter und derartige Sicherheitsrisiken im Code unkenntlich gemacht.