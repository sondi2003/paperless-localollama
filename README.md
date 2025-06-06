Would you like to help me with this project?
then please contact me.

Möchtest du mir bei diesem Projekt helfen?
Dann melde dich doch bitte bei mir.

# paperless-localollama


# Dokumentenanalyse mit OLLama und Paperless-ngx

Dieses Projekt bietet ein Python-Skript, das Dokumente in einer [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx)-Instanz automatisiert analysiert und kategorisiert, unterstützt durch [OLLama](https://ollama.ai/). Mit diesem Tool können Dokumenttitel und Tags basierend auf einer KI-gestützten Analyse des Inhalts aktualisiert werden.

## Funktionen
- **Automatische Verbindung** zur Paperless-ngx-API
- **KI-gestützte Analyse** des Dokumentinhalts mit OLLama (Modell `llama3.2:3b`)
- **Extraktion von Titeln und Tags**
- **Hinzufügen und Aktualisieren** von Tags und Titeln in Paperless-ngx
- Konfigurierbare Optionen, einschließlich Begrenzung der zu analysierenden Dokumente

## Voraussetzungen
- Python 3.9 oder neuer
- [Requests-Bibliothek](https://pypi.org/project/requests/)
- [OLLama CLI](https://ollama.ai/)
- Eine laufende Instanz von Paperless-ngx
- Ein gültiger API-Key für die Paperless-ngx-Instanz

## Installation
1. **Repository klonen:**
   ```bash
   git clone <REPOSITORY-URL>
   cd <REPOSITORY-NAME>
   ```

2. **Abhängigkeiten installieren:**
   ```bash
   pip install requests
   ```

3. **OLLama CLI installieren:**
   Folge den [Installationsanweisungen von OLLama](https://ollama.ai/download).

## Konfiguration
1. **API-Details anpassen:** Bearbeite die Variablen `PAPERLESS_URL` und `API_KEY` im Skript, um die URL und den API-Key deiner Paperless-ngx-Instanz anzugeben.
2. **OLLama-Modell:** Stelle sicher, dass das Modell `llama3.2:3b` in deiner OLLama-Instanz verfügbar ist.
3. **Optionen konfigurieren:**
   - `SAVE_CHANGES`: Ändere auf `False`, um Änderungen in Paperless-ngx zu deaktivieren.
   - `MAX_DOCUMENTS`: Lege die maximale Anzahl der zu analysierenden Dokumente fest.

## Nutzung
1. **Skript ausführen:**
   ```bash
   python3 paperless-localollama.py
   ```

2. **Ablauf:**
   - Dokumente ohne den Tag `AI` werden von Paperless-ngx abgerufen.
   - Die Dokumentinhalte werden von OLLama analysiert.
   - Titel und Tags werden basierend auf der Analyse aktualisiert.

## Beispieleingabe
Ein typischer Prompt für die Analyse:
```
Erstellen Sie basierend auf dem Dokumentinhalt einen prägnanten Titel und 1-4 relevante Tags. 
Antworten Sie ausschließlich im JSON-Format:
{
  "title": "<Titel>",
  "tags": ["<Tag1>", "<Tag2>"]
}
```

## Fehlerbehebung
- **Timeout-Fehler bei OLLama:** Erhöhe den `timeout`-Wert in der Funktion `analyze_with_ollama`.
- **API-Probleme:** Überprüfe die URL und den API-Key für Paperless-ngx.

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz. Details findest du in der Datei `LICENSE`.

---

Möchtest du mich bei diesem Projekt unterstützen?  
Ich bin kein Entwickler und würde mich über Hilfe freuen, um dieses Projekt weiter zu verbessern.  
Bitte melde dich, wenn du Interesse hast – ich freue mich auf deine Unterstützung!

---

# Document Analysis with OLLama and Paperless-ngx

This project provides a Python script for automating document analysis and categorization in a [Paperless-ngx](https://github.com/paperless-ngx/paperless-ngx) instance, supported by [OLLama](https://ollama.ai/). It allows for updating document titles and tags based on AI-driven content analysis.

## Features
- **Automatic connection** to the Paperless-ngx API
- **AI-driven analysis** of document content using OLLama (`llama3.2:3b` model)
- **Extraction of titles and tags**
- **Adding and updating** tags and titles in Paperless-ngx
- Configurable options, including limiting the number of analyzed documents

## Requirements
- Python 3.9 or newer
- [Requests library](https://pypi.org/project/requests/)
- [OLLama CLI](https://ollama.ai/)
- A running instance of Paperless-ngx
- A valid API key for your Paperless-ngx instance

## Installation
1. **Clone the repository:**
   ```bash
   git clone <REPOSITORY-URL>
   cd <REPOSITORY-NAME>
   ```

2. **Install dependencies:**
   ```bash
   pip install requests
   ```

3. **Install OLLama CLI:**
   Follow the [OLLama installation guide](https://ollama.ai/download).

## Configuration
1. **Adjust API details:** Edit the variables `PAPERLESS_URL` and `API_KEY` in the script to set your Paperless-ngx instance's URL and API key.
2. **OLLama model:** Ensure the `llama3.2:3b` model is available in your OLLama instance.
3. **Configure options:**
   - `SAVE_CHANGES`: Set to `False` to disable changes in Paperless-ngx.
   - `MAX_DOCUMENTS`: Limit the number of documents to analyze.

## Usage
1. **Run the script:**
   ```bash
   python3 paperless-localollama.py
   ```

2. **Workflow:**
   - The script fetches documents without the `AI` tag from Paperless-ngx.
   - Document content is analyzed by OLLama.
   - Titles and tags are updated based on the analysis.

## Sample Input
A typical prompt for analysis:
```
Generate a concise title and 1-4 relevant tags based on the document content. 
Respond strictly in JSON format:
{
  "title": "<Title>",
  "tags": ["<Tag1>", "<Tag2>"]
}
```

## Troubleshooting
- **OLLama timeout error:** Increase the `timeout` value in the `analyze_with_ollama` function.
- **API issues:** Double-check the Paperless-ngx URL and API key.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Would you like to support me with this project?  
I am not a developer and would greatly appreciate help to improve this project.  
Feel free to reach out if you're interested – your support means a lot!

