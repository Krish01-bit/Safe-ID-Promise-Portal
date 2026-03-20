# SIP (Safe ID Promise) — Identity Verification Portal

A privacy-first AI-based identity verification system for Aadhaar and PAN cards that performs secure OCR, data extraction, and fraud detection without exposing sensitive data to external services.

---

## Overview

SIP (Safe ID Promise) is an AI-powered identity verification system designed for secure digital onboarding. It processes identity documents locally using computer vision and rule-based validation to ensure data privacy, accuracy, and fraud prevention.

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
git clone https://github.com/Krish01-bit/sip-portal.git
cd sip-portal
pip install -r requirements.txt
python app.py
```

## Open in browser:

http://127.0.0.1:5000

## Output

Extracted identity details

Risk score

Verification status:
VERIFIED
FLAGGED
REJECTED

## Team

Harisaran K — AI / Computer Vision
Krish Agarwal — OCR & Data Extraction
Manogar G — Fraud Detection & Decision Engine
Abinaya T — Frontend
Menaka G — Backend / Integration


