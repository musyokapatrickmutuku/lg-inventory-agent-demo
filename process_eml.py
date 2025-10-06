# process_eml.py
import os
import sqlite3
import re
from email import policy
from email.parser import BytesParser
from datetime import datetime

ROOT = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT, "demo.db")
SAMPLES_DIR = os.path.join(ROOT, "eml_samples")

RULES = [
    (r'\brfq\b|request for quotation|request a quotation|quotation', 'RFQ'),
    (r'\binvoice\b|paid|receipt|bill', 'Finance'),
    (r'\brefund\b|faulty|broken|complaint|repair|replace|warranty', 'Complaint'),
    (r'\border\b|purchase|buy|sale|sold', 'Sales'),
    (r'\bshipment\b|delivered|tracking|shipped', 'Shipment'),
]

def classify_text(text):
    txt = (text or "").lower()

    for pattern, label in RULES:
        match = re.search(pattern, txt, flags=re.IGNORECASE)
        if match:
            keyword = match.group(0)
            explanation = f"Matched rule for '{label}' (keyword: '{keyword}')"
            return label, 0.95, explanation

    # Deterministic fallback (mock LLM)
    if 'please' in txt and 'quotation' in txt:
        return 'RFQ', 0.70, "Fallback: Found 'please' + 'quotation' in text"
    if 'flicker' in txt or 'screen' in txt:
        return 'Complaint', 0.70, "Fallback: Found 'flicker' or 'screen' in text"

    return 'Unknown', 0.40, "No matching keyword found"



def process_file(path):
    from email import policy
    from email.parser import BytesParser
    import sqlite3, os
    from datetime import datetime

    with open(path, 'rb') as fp:
        msg = BytesParser(policy=policy.default).parse(fp)

    subject = msg['subject'] or ''
    sender = str(msg.get('from') or '')

    # --- FIX: handle both multipart and single-part emails ---
    if msg.is_multipart():
        parts = []
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                parts.append(part.get_payload(decode=True).decode(errors="ignore"))
        body_text = "\n".join(parts)
    else:
        # Single-part: get the raw payload directly
        body_text = msg.get_payload(decode=True).decode(errors="ignore")

    # combine subject + body for classification
    label, conf, explanation = classify_text(subject + "\n" + body_text)


    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO emails (filename, subject, sender, body, label, confidence, processed_at) VALUES (?,?,?,?,?,?,?)",
        (os.path.basename(path), subject, sender, body_text, label, conf, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()
    return label, conf


def process_all():
    if not os.path.isdir(SAMPLES_DIR):
        print("No eml_samples/ folder found. Create it and add .eml files.")
        return
    for fname in sorted(os.listdir(SAMPLES_DIR)):
        if fname.lower().endswith('.eml'):
            full = os.path.join(SAMPLES_DIR, fname)
            lbl, conf = process_file(full)
            print(f"Processed {fname}: label={lbl}, confidence={conf}")

if __name__ == '__main__':
    process_all()
