import os
import uuid
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from image_module import process_image
from extraction_module import extract_document_data
from verification_module import verify_document

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'temp_uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
hash_database = set()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def home_alt():
    return render_template('index.html')

@app.route('/verification.html')
def verification_page():
    return render_template('verification.html')

@app.route('/api/verify', methods=['POST'])
def verify_api():
    try:
        if 'id_document' not in request.files or 'selfie' not in request.files:
            return jsonify({"error": "Missing ID document or selfie"}), 400

        id_file = request.files['id_document']
        selfie_file = request.files['selfie']
        
        # Get user's dropdown selection
        doc_type_input = request.form.get('doc_type', 'UNKNOWN').upper()
        if "AADHAAR" in doc_type_input:
            doc_type_input = "AADHAAR"
        elif "PAN" in doc_type_input:
            doc_type_input = "PAN"

        id_path = os.path.join(UPLOAD_FOLDER, f"id_{uuid.uuid4().hex}.jpg")
        selfie_path = os.path.join(UPLOAD_FOLDER, f"selfie_{uuid.uuid4().hex}.jpg")
        
        id_file.save(id_path)
        selfie_file.save(selfie_path)

        # --- MODULE 1: Image Processing ---
        image_result = process_image(id_path)
        id_face = image_result["face_image"] 
        detected_doc_type = image_result["document_type"]
        ocr_text = image_result["ocr_text"]

        # --- MODULE 2: Data Extraction ---
        # We extract first so we can use the strict regex patterns for the mismatch check
        extracted_data = extract_document_data(ocr_text, id_path, doc_type_input)

        pan_found = extracted_data.get("pan_number")
        aadhaar_found = extracted_data.get("aadhaar_number")

        # --- 🚨 BULLETPROOF MISMATCH CHECK 🚨 ---
        
        # 1. Check based on extracted IDs (Most reliable)
        if doc_type_input == "PAN" and aadhaar_found and not pan_found:
            os.remove(id_path)
            os.remove(selfie_path)
            return jsonify({"error": "Security Alert: You selected PAN Card but uploaded an Aadhaar Card!"}), 400
            
        if doc_type_input == "AADHAAR" and pan_found and not aadhaar_found:
            os.remove(id_path)
            os.remove(selfie_path)
            return jsonify({"error": "Security Alert: You selected Aadhaar Card but uploaded a PAN Card!"}), 400

        # 2. Check based on OCR Text Keywords (Fallback)
        if detected_doc_type != "UNKNOWN" and detected_doc_type != doc_type_input:
            os.remove(id_path)
            os.remove(selfie_path)
            return jsonify({"error": f"Mismatch Detected: You selected {doc_type_input} but uploaded a {detected_doc_type}."}), 400

        # Handle cases where no face is found on the ID card
        if id_face is None:
            os.remove(id_path)
            os.remove(selfie_path)
            return jsonify({"error": "Could not detect a face on the provided ID document."}), 400

        # --- MODULE 3: Fraud Detection + Decision ---
        final_result, audit_log = verify_document(
            image_path=id_path,
            extracted_data=extracted_data,
            document_type=doc_type_input,
            hash_database=hash_database,
            id_face=id_face,
            selfie_path=selfie_path
        )

        os.remove(id_path)
        os.remove(selfie_path)

        return jsonify(final_result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)