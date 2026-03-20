import re
import cv2
from pyzbar.pyzbar import decode

# -----------------------------
# 1️⃣ Name Extraction - HALLUCINATION FILTER ADDED
# -----------------------------
def extract_name(text):
    
    # Aggressively strip out Aadhaar headers, languages, and OCR glitches
    junk_words = r"(?i)\b(GOV[A-Z]*|IND[A-Z]*|TAX|DEP[A-Z]*|FATH[A-Z]*|DOB|DATE|YEAR|MALE|FEMALE|GENDER|OOW|NOIMALD|PAN|CARD|SIGNATURE|VALID|MULT|COD|DMATSD|INCOME|ACCOUNT|PERMANENT|NUMBER|TAU|BAN|MERI|PEHCHAN|UNIQUE|AUTHORITY|IDENTIFICATION)\b"
    clean_text = re.sub(junk_words, " ", text)
    
    # Strategy A: Explicit "Name" prefix
    pattern_explicit = r"(?:Name|Nane|NAME)[\s:/-]+([A-Za-z]{3,}\s+[A-Za-z]{3,}(?:\s+[A-Za-z]{3,})?)"
    match = re.search(pattern_explicit, clean_text)
    if match:
        return match.group(1).title()

    # Strategy B: Implicit Name format 
    # Must be 2-3 words. (Increased minimum length slightly to avoid 2-letter glitches)
    pattern_implicit = r"\b([A-Z][a-z]{2,14}\s+[A-Z][a-z]{2,14}(?:\s+[A-Z][a-z]{2,14})?|[A-Z]{3,14}\s+[A-Z]{3,14}(?:\s+[A-Z]{3,14})?)\b"
    matches = re.findall(pattern_implicit, clean_text)
    
    for m in matches:
        # A real name must NOT have numbers AND must have vowels. This kills OCR gibberish!
        if not any(char.isdigit() for char in m) and re.search(r'[aeiouAEIOU]', m):
            return m.title()
            
    return None


# -----------------------------
# 2️⃣ PAN Extraction
# -----------------------------
def extract_pan(text):
    pattern = r"[A-Z]{5}\s?[0-9]{4}\s?[A-Z]"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group().replace(" ", "").upper()
    return None


# -----------------------------
# 3️⃣ Aadhaar Extraction
# -----------------------------
def extract_aadhaar(text):
    pattern = r"\d{4}[\s-]?\d{4}[\s-]?\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group().replace("-", " ")
    return None


# -----------------------------
# 4️⃣ Date of Birth Extraction
# -----------------------------
def extract_dob(text):
    pattern = r"\d{2}[-/\.]\d{2}[-/\.]\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group()
        
    pattern_yob = r"(?:YOB|Year of Birth)[\s:]*(\d{4})"
    match_yob = re.search(pattern_yob, text, re.IGNORECASE)
    if match_yob:
        return match_yob.group(1)
        
    return None


# -----------------------------
# 5️⃣ QR Code Decoder
# -----------------------------
def decode_qr(image_path):
    image = cv2.imread(image_path)
    decoded_objects = decode(image)
    for obj in decoded_objects:
        return obj.data.decode("utf-8")
    return None


# -----------------------------
# 6️⃣ Field Validation
# -----------------------------
def validate_fields(pan, aadhaar):
    validation = {"pan_valid": False, "aadhaar_valid": False}
    if pan: validation["pan_valid"] = True
    if aadhaar: validation["aadhaar_valid"] = True
    return validation


# -----------------------------
# Main Extraction Pipeline
# -----------------------------
def extract_document_data(text, image_path, document_type):
    name = extract_name(text)
    pan = extract_pan(text)
    aadhaar = extract_aadhaar(text)
    dob = extract_dob(text)

    qr_data = decode_qr(image_path) if document_type == "AADHAAR" else None
    validation = validate_fields(pan, aadhaar)

    return {
        "name": name,
        "pan_number": pan,
        "aadhaar_number": aadhaar,
        "dob": dob,
        "qr_data": qr_data,
        "validation": validation
    }