import os
import requests
import subprocess
import json
import re
import random

# Paperless-ngx API-Details aus Umgebungsvariablen beziehen
PAPERLESS_URL = os.getenv("PAPERLESS_URL")
API_KEY = os.getenv("API_KEY")

if not PAPERLESS_URL or not API_KEY:
    raise EnvironmentError(
        "PAPERLESS_URL and API_KEY environment variables must be set"
    )
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Accept": "application/json; version=6"
}

# OLLama-Befehl
OLLAMA_COMMAND = "ollama run llama3.2:3b"

# Konfiguration: Speichern aktivieren oder deaktivieren
SAVE_CHANGES = True  # Ändere auf False, um Änderungen zu deaktivieren
MAX_DOCUMENTS = 0  # 0 für alle Dokumente, oder positive Zahl für Limitierung
COLORS = ["#FF5733", "#33FF57", "#3357FF", "#FF33A1", "#A1FF33", "#33A1FF"]

def sanitize_tag(tag_name):
    """Bereinigt den Tag-Namen, um API-kompatible Tags zu erstellen."""
    if not tag_name or not isinstance(tag_name, str):
        return None
    sanitized_tag = re.sub(r"[^a-zA-Z0-9äöüÄÖÜß ]", "", tag_name).strip()
    return sanitized_tag[:50] if sanitized_tag else None

def get_all_tags():
    """Holt alle Tags aus der Paperless-ngx API."""
    all_tags = []
    url = f"{PAPERLESS_URL}/api/tags/"
    
    while url:
        try:
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            all_tags.extend(data.get("results", []))
            url = data.get("next")  # URL der nächsten Seite abrufen
        except Exception as e:
            print(f"Fehler beim Abrufen der Tags: {e}")
            break
    
    return all_tags

def find_tag_id(tag_name, all_tags):
    """Findet die ID eines vorhandenen Tags anhand seines Namens."""
    sanitized_tag = sanitize_tag(tag_name)
    if not sanitized_tag:
        print(f"Ungültiges oder leeres Tag: {tag_name}")
        return None
    
    for tag in all_tags:
        if "name" in tag and tag["name"].lower() == sanitized_tag.lower():
            return tag["id"]
    return None

def create_tag(tag_name):
    """Erstellt ein neues Tag in Paperless-ngx."""
    sanitized_tag = sanitize_tag(tag_name)
    if not sanitized_tag:
        print(f"Ungültiges Tag: {tag_name}")
        return None
    
    try:
        data = {"name": sanitized_tag, "color": random.choice(COLORS)}
        response = requests.post(f"{PAPERLESS_URL}/api/tags/", headers=HEADERS, json=data)
        response.raise_for_status()
        return response.json()["id"]
    except Exception as e:
        print(f"Fehler beim Erstellen von Tag '{sanitized_tag}': {e}")
        return None

def add_tags_to_document(doc_id, tag_ids):
    """Fügt Tags zu einem Dokument in Paperless-ngx hinzu."""
    if not tag_ids:
        print("Keine Tags zum Hinzufügen gefunden. Vorgang abgebrochen.")
        return
    
    tags_data = {
        "documents": [doc_id],
        "method": "modify_tags",
        "parameters": {
            "add_tags": tag_ids,
            "remove_tags": []  # Wichtig: Leeres Array hinzufügen
        }
    }
    
    try:
        print(f"Anfrage-Daten: {json.dumps(tags_data, indent=2)}")  # Debugging
        response = requests.post(
            f"{PAPERLESS_URL}/api/documents/bulk_edit/", headers=HEADERS, json=tags_data
        )
        response.raise_for_status()
        print(f"Tags erfolgreich zu Dokument {doc_id} hinzugefügt.")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Hinzufügen der Tags zu Dokument {doc_id}: {e}")
        if e.response is not None:
            print(f"API-Fehlerdetails: {e.response.text}")

def update_document_title(doc_id, new_title):
    """Aktualisiert den Titel eines Dokuments in Paperless-ngx."""
    if len(new_title) > 255:
        new_title = new_title[:255]  # Titel auf 255 Zeichen beschränken
    
    data = {"title": new_title}
    
    try:
        print(f"Setze neuen Titel für Dokument ID {doc_id}: {new_title}")
        response = requests.patch(f"{PAPERLESS_URL}/api/documents/{doc_id}/", headers=HEADERS, json=data)
        response.raise_for_status()
        print(f"Dokumenttitel erfolgreich aktualisiert: {new_title}")
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Aktualisieren des Titels für Dokument ID {doc_id}: {e}")
        if e.response is not None:
            print(f"API-Fehlerdetails: {e.response.text}")

def process_document(doc_id, new_title, tag_names):
    """Aktualisiert Titel und Tags eines Dokuments in Paperless-ngx."""
    all_tags = get_all_tags()
    tag_ids = []

    # Stelle sicher, dass "AI" in den tag_names ist
    if "AI" not in tag_names:
        tag_names.append("AI")

    for tag_name in tag_names:
        if not isinstance(tag_name, str):  # Nur Strings verarbeiten
            print(f"Ignoriere ungültiges Tag: {tag_name}")
            continue

        tag_id = find_tag_id(tag_name, all_tags)
        if not tag_id:  # Tag existiert nicht, also erstellen
            tag_id = create_tag(tag_name)
        if tag_id:
            tag_ids.append(tag_id)
        else:
            print(f"Fehler beim Verarbeiten von Tag: {tag_name}")

    # Tags aktualisieren
    if tag_ids:
        add_tags_to_document(doc_id, tag_ids)
    else:
        print(f"Keine gültigen Tags für Dokument ID {doc_id} gefunden.")

    # Titel aktualisieren
    if new_title:
        update_document_title(doc_id, new_title)

def get_documents_without_ai():
    """Ruft Dokumente ohne den Tag 'AI' von Paperless-ngx ab."""
    print("Verbinde mit Paperless-ngx API ...")
    documents = []
    try:
        # Hole zuerst die AI-Tag-ID
        ai_tag_response = requests.get(f"{PAPERLESS_URL}/api/tags/?name=AI", headers=HEADERS)
        ai_tag_response.raise_for_status()
        ai_tag_data = ai_tag_response.json()
        
        if not ai_tag_data['count']:
            print("AI-Tag nicht gefunden. Erstelle neues AI-Tag...")
            ai_tag_response = requests.post(f"{PAPERLESS_URL}/api/tags/", headers=HEADERS, json={"name": "AI"})
            ai_tag_response.raise_for_status()
            ai_tag_id = ai_tag_response.json()["id"]
        else:
            ai_tag_id = ai_tag_data['results'][0]['id']

        # Hole alle Dokumente ohne AI-Tag, iteriere über alle Seiten
        url = f"{PAPERLESS_URL}/api/documents/?tags__exclude={ai_tag_id}&ordering=-added"
        while url:
            if MAX_DOCUMENTS > 0:
                url += f"&page_size={MAX_DOCUMENTS}"
            
            response = requests.get(url, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            documents.extend(data.get("results", []))
            url = data.get("next")

        print(f"Erfolgreich verbunden. {len(documents)} Dokumente ohne AI-Tag gefunden.")
    except Exception as e:
        print(f"Fehler bei der Verbindung mit Paperless-ngx: {e}")
    return documents

def analyze_with_ollama(content, existing_tags, timeout=60):
    """Analysiert den Dokumentinhalt mit OLLama und bezieht bestehende Tags in die Analyse ein."""
    existing_tags_str = ", ".join([tag["name"] for tag in existing_tags if "name" in tag])
    
    prompt = (
        "Sie sind ein personalisierter Dokumentenanalysator. Ihre Aufgabe ist es, Dokumente zu analysieren und relevante Informationen zu extrahieren.\n\n"
        "Bitte antworten Sie NUR im JSON-Format mit folgendem Schema:\n"
        "{\n"
        '  "title": "Der generierte Titel",\n'
        '  "tags": ["Tag1", "Tag2", "Tag3"]\n'
        "}\n\n"
        "Es gibt eine Liste bestehender Tags, die bereits verwendet werden. Bitte priorisieren Sie diese Tags, wenn sie zum Inhalt passen.\n\n"
        f"Bestehende Tags: {existing_tags_str}\n\n"
        "Wichtige Regeln:\n"
        "1. Der Titel soll prägnant und aussagekräftig sein.\n"
        "2. Wählen Sie 1-4 relevante thematische Tags.\n"
        "3. Bevorzugen Sie existierende Tags.\n"
        "4. Erstellen Sie neue Tags nur wenn keine passenden existieren.\n\n"
        f"Dokumentinhalt: {content}"
    )

    print("Starte Analyse mit OLLama ...")
    command = ["ollama", "run", "llama3.2:3b"]
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    try:
        stdout, stderr = process.communicate(input=prompt, timeout=timeout)

        if process.returncode != 0:
            print(f"OLLama Fehler: {stderr.strip()}")
            raise RuntimeError(f"OLLama Fehler: {stderr.strip()}")

        # Versuche JSON aus der Antwort zu extrahieren
        response_text = stdout.strip()
        print(f"OLLama Rohantwort: {response_text}")  # Debug-Ausgabe
        
        # Suche nach JSON-Struktur in der Antwort
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            raise ValueError("Keine JSON-Struktur in der Antwort gefunden")
            
        json_str = json_match.group(0)
        analysis_result = json.loads(json_str)
        
        # Validiere das Ergebnis
        if not isinstance(analysis_result, dict):
            raise ValueError("Ungültiges Antwortformat")
        
        if "title" not in analysis_result or "tags" not in analysis_result:
            raise ValueError("Fehlende erforderliche Felder in der Antwort")
            
        # Stelle sicher, dass Tags eine Liste ist
        if not isinstance(analysis_result["tags"], list):
            analysis_result["tags"] = [analysis_result["tags"]]
            
        print(f"Extrahierte Daten: {analysis_result}")  # Debug-Ausgabe
        return analysis_result

    except subprocess.TimeoutExpired:
        process.kill()
        print(f"OLLama Timeout nach {timeout} Sekunden.")
        raise RuntimeError("OLLama hat zu lange gebraucht.")
    except json.JSONDecodeError as e:
        print(f"Fehler beim Parsen der JSON-Antwort: {e}")
        raise
    except Exception as e:
        print(f"Fehler bei der Analyse mit OLLama: {e}")
        raise

def main():
    # Bestehende Tags abrufen
    print("Lade vorhandene Tags aus Paperless-ngx ...")
    existing_tags = get_all_tags()
    if not existing_tags:
        print("Es konnten keine vorhandenen Tags abgerufen werden. Abbruch.")
        return
    print(f"{len(existing_tags)} vorhandene Tags geladen.")

    # Dokumente ohne 'AI'-Tag abrufen
    documents = get_documents_without_ai()
    if not documents:
        print("Keine Dokumente ohne 'AI'-Tag gefunden.")
        return

    print(f"{len(documents)} Dokumente ohne 'AI'-Tag werden analysiert:")
    for doc in documents:
        print(f"  - {doc['title']} (ID: {doc['id']})")

    for idx, doc in enumerate(documents, start=1):
        doc_id = doc["id"]
        title = doc["title"]
        content = doc["content"]
        current_tags = doc.get("tags", [])

        if not content or content.strip() == "":
            print(f"Dokument ID {doc_id} hat keinen Inhalt. Überspringe.")
            continue

        print(f"\n[{idx}/{len(documents)}] Verarbeite Dokument ID {doc_id}: {title}")

        try:
            # OLLama mit bestehenden Tags aufrufen
            analysis_data = analyze_with_ollama(content, existing_tags)
            
            if SAVE_CHANGES:
                # Alle Änderungen in process_document durchführen
                process_document(doc_id, analysis_data["title"], analysis_data["tags"])
            else:
                print("Speichern deaktiviert. Änderungen werden nicht an Paperless-ngx übergeben.")
        except Exception as e:
            print(f"Fehler bei der Verarbeitung von Dokument ID {doc_id}: {e}")

if __name__ == "__main__":
    main()
