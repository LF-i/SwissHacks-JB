# 🛡️ Julius Baer Client Document Validator

## Overview

This project was developed as part of the Julius Baer Hackathon. The challenge was to **automatically verify and validate client information** across multiple documents provided in different formats.

The goal is to help streamline client onboarding by:
- **Extracting relevant data** from client-submitted documents.
- **Checking for consistency** within each document.
- **Cross-validating information** across all submitted documents.
- **Accepting or rejecting** the client based on rule-based and machine learning evaluation.

---

## 🔍 Use Case

Each client provides **four key documents** in different formats:
- Passport (PNG image)
- Account opening form (PDF)
- Client profile (DOCX)
- Client activity description (TXT)

Our system:
1. Extracts structured information from each file.
2. Validates the internal consistency of each document.
3. Compares information across all documents.
4. Flags inconsistencies and decides to **accept or reject** the client.
5. For non-rejected clients, a **Random Forest model** performs additional checks to catch inconsistencies not explicitly covered by rules.

---

## 🧠 How It Works

### 🔧 File-by-File Breakdown

- **`backend.py`**  
  Orchestrates the end-to-end process: document parsing, rule-based validation, cross-file consistency checks, and ML-based validation.

- **`globals.py`**  
  Stores the global variable indicating whether the client has been accepted or rejected.

- **`passport.py`**  
  Uses deep learning to extract and validate information from the client’s passport (PNG). Ensures internal consistency (e.g., matching country codes, date formats, etc.).

- **`profile.py`**  
  Parses and validates the client’s profile form (DOCX), applying rule-based logic to ensure all fields make sense and are self-consistent.

- **`account.py`**  
  Extracts structured data from the account opening form (PDF) and checks it against predefined logical rules.

- **`training_forest.py`**  
  Prepares the dataset from validated document information and trains a **Random Forest classifier**. This model identifies clients whose information may seem consistent on the surface but contains deeper-level irregularities.

---

## ✅ Decision Logic

1. **Hard-coded checks** are applied:
   - Internal consistency within each document.
   - Cross-document consistency for shared fields.

2. If the client passes all rule-based checks:
   - **Machine Learning validation** (Random Forest) is applied for final verification.

3. Based on the result, the client is either **accepted** or **rejected**.

---

## 📁 Folder Structure

