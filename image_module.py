import cv2
import numpy as np
import easyocr
import re

# Initialize OCR reader
reader = easyocr.Reader(['en'])

# -----------------------------
# 1️⃣ Image Quality Check
# -----------------------------
def check_image_quality(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()

    if blur_score < 100:
        return "poor"
    else:
        return "good"

# -----------------------------
# 2️⃣ Image Preprocessing
# -----------------------------
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return image, thresh

# -----------------------------
# 3️⃣ OCR Text Extraction
# -----------------------------
def extract_text(processed_image):
    results = reader.readtext(processed_image)
    text_list = [detection[1] for detection in results]
    text = " ".join(text_list)
    return text

# -----------------------------
# 4️⃣ Document Type Detection - UPGRADED
# -----------------------------
def detect_document_type(text):
    text = text.upper()

    # Look for explicit 12-digit Aadhaar pattern or strong keywords
    if re.search(r"\d{4}[\s-]?\d{4}[\s-]?\d{4}", text) or "AADHAAR" in text or "UIDAI" in text or "UNIQUE IDENTIFICATION" in text:
        return "AADHAAR"
        
    # Look for explicit PAN pattern (ABCDE1234F) or strong keywords
    if re.search(r"[A-Z]{5}\s?[0-9]{4}\s?[A-Z]", text) or "INCOME TAX" in text or "PERMANENT ACCOUNT" in text:
        return "PAN"
        
    return "UNKNOWN"

# -----------------------------
# 5️⃣ Face Detection + Extraction
# -----------------------------
def detect_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    return len(faces) > 0

def extract_face(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    face = image[y:y+h, x:x+w]
    return face

# -----------------------------
# Main Function for Module
# -----------------------------
def process_image(image_path):
    image, processed = preprocess_image(image_path)
    quality = check_image_quality(image)
    text = extract_text(processed)
    document_type = detect_document_type(text)
    face = extract_face(image)

    result = {
        "document_type": document_type,
        "image_quality": quality,
        "face_detected": face is not None,
        "face_image": face,
        "ocr_text": text
    }

    return result