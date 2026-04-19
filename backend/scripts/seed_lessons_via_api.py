import json
import argparse
import requests
from docx import Document

def extract_json_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = "".join([para.text for para in doc.paragraphs]).strip()
        start = full_text.find('[')
        end = full_text.rfind(']') + 1
        return json.loads(full_text[start:end])
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

def seed(file_path, url):
    data = extract_json_from_docx(file_path)
    if not data: return

    print(f"🌱 Seeding {file_path}...")
    for item in data:
        # Normalizing keys: supports 'sms_text' or 'sms_content'
        payload = {
            "code": item.get("code"),
            "title": item.get("title"),
            "content": item.get("content"),
            "language": item.get("language"),
            "theme": item.get("theme") or item.get("module"),
            "sms_text": item.get("sms_text") or item.get("sms_content")
        }
        
        try:
            res = requests.post(f"{url}/lessons/", json=payload)
            if res.status_code in [200, 201]:
                print(f" ✅ {payload['code']} ({payload['language']})")
            else:
                print(f" ❌ {payload['code']} error: {res.text}")
        except Exception as e:
            print(f" 🛑 Connection error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--url", default="http://localhost:8000")
    args = parser.parse_args()
    seed(args.file, args.url)