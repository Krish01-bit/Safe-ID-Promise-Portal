# SIP (Safe ID Promise) — Identity Verification Portal

A privacy-first AI-based identity verification system for Aadhaar and PAN cards that performs secure OCR, data extraction, and fraud detection without exposing sensitive data to external services.

---

## Overview

SIP (Safe ID Promise) is an AI-powered identity verification system designed for secure digital onboarding. It processes identity documents locally using computer vision and rule-based validation to ensure data privacy, accuracy, and fraud prevention.

---

## Problem Statement

Traditional identity verification systems rely on manual checks or external AI services, leading to slow processing, inconsistent accuracy, and privacy risks due to exposure of sensitive user data.

There is a need for a secure, automated, and privacy-first solution that can verify Aadhaar and PAN documents locally while detecting fraud and ensuring reliable digital onboarding.

---

## Features

- Face verification using DeepFace (Facenet)  
- OCR-based data extraction using EasyOCR  
- Aadhaar & PAN detection using regex  
- Tampering detection using Error Level Analysis (ELA)  
- Duplicate detection using image hashing (MD5)  
- Document type mismatch detection  
- Risk scoring and decision engine  
- QR code decoding (Aadhaar support)  

---

## Workflow

1. Upload Aadhaar or PAN card  
2. Capture live selfie  
3. Extract text and detect document type  
4. Validate fields (Name, DOB, ID numbers)  
5. Perform fraud checks:  
   - Tampering detection  
   - Duplicate detection  
   - Face verification  
6. Generate final result:  
   - VERIFIED  
   - FLAGGED  
   - REJECTED  

---

## Core Concept

- Privacy-first processing (no external AI/LLM usage)  
- End-to-end verification pipeline  
- Explainable rule-based decision system  
- Integrated fraud detection beyond OCR  

---

## Tech Stack

**Backend**
- Python, Flask, Flask-CORS  

**Computer Vision & AI**
- OpenCV  
- DeepFace (Facenet)  
- EasyOCR  
- Pillow  

**Other**
- NumPy  
- Gunicorn  

---

## Setup & Run

```bash
git clone https://github.com/Krish01-bit/sip-identity-verification.git
cd sip-identity-verification
pip install -r requirements.txt
python app.py
```
Open in browser:

http://127.0.0.1:5000

---

## Live Demo

https://krish014-sip-portal.hf.space

---

## Output

- Extracted identity details  
- Risk score  
- Verification status:  
  - VERIFIED  
  - FLAGGED  
  - REJECTED  

---

## Limitations

### Input Constraints

- Requires properly aligned and clearly visible ID images  
- Sensitive to lighting conditions (glare, shadows)  
- Face detection may fail with occlusions (mask, glasses, side angles)  
- Supports standard image formats only (JPEG/PNG)  

### Output Constraints

- Results are displayed via UI (no structured API response yet)  
- Limited explainability for borderline face match scores  
- No persistent storage → results are not retained after session  

### Hardware & Hosting

- Runs on CPU-based environment → higher latency (5–10 seconds)  
- Cold start delay due to free-tier hosting  

### AI & Model Constraints

- OCR accuracy affected by glare, multilingual text, or damaged documents  
- Face verification affected by aging, lighting, and pose variations  
- No liveness detection → vulnerable to spoofing  

### System Architecture

- Stateless design → no audit logs for compliance  
- Not optimized for high concurrent user traffic  

---

## Team

- Harisaran K — AI / Computer Vision  
- Krish Agarwal — OCR & Data Extraction  
- Manogar G — Fraud Detection & Decision Engine  
- Abinaya T — Frontend  
- Menaka G — Backend / Integration  

## Note

Developed as part of Hackzen’26.

---

## Future Improvements

- GPU acceleration for faster inference  
- Liveness detection to prevent spoofing  
- Improved OCR robustness for real-world conditions  
- Scalable deployment while maintaining privacy-first design  
