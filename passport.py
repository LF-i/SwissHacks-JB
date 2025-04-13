#This script uses a machine learning model to read data from the passport file. It structures it into a dictionary
#and checks if there are missing entries or if it's expired

import cv2
import pytesseract
from datetime import datetime, timedelta
import globals
import re
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

passport_data = {}

not_verify_name = 0
not_verify_number = 0

def passport_op(image_path):

# Load image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError("Image not found. Check the file path.")

    # Resize for consistent cropping
    image = cv2.resize(image, (512, 400))

    # Field crop coordinates (MRZ removed)
    fields = {
        "Nationality": (15, 33, 460, 50),
        "PassportType": (20, 60, 120, 95),
        #"Code": (160, 70, 220, 105),
        "Passport_No": (310, 70, 430, 95),
        "Surname": (20, 132, 110, 155),
        "Given_Names": (170, 132, 370, 155),
        "Citizenship": (170, 185, 370, 215),
        "Sex": (20, 240, 50, 260),
        "Birth Date": (20, 185, 140, 215),
        "Issue Date": (170, 240, 300, 260),
        "Expiry Date": (170, 280, 300, 300),
        "Signature": (320, 280, 460, 335),
    }

    # OCR and save
    ocr_results = {}

    
    not_verify_name = 0
    not_verify_number = 0

    for field, (x1, y1, x2, y2) in fields.items():
        cropped = image[y1:y2, x1:x2]
        gray = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        # Retry until valid
        retries = 5
        while retries > 0:
            text = pytesseract.image_to_string(thresh, config='--psm 6').strip()

            # Validate name fields: only uppercase letters and spaces
            if field in ["Surname", "Given_Names"]:
                if re.fullmatch(r"[A-Z\s]+", text):
                    break  # Valid name
                else:
                    not_verify_name = 1
                    print("Name corrupted")

            # Validate exact date format: dd-MMM-yyyy (e.g., 15-APR-2025)
            elif field in ["Birth Date", "Issue Date", "Expiry Date"]:
                try:
                    datetime.strptime(text, "%d-%b-%Y")
                    break  # Valid date
                except:
                    pass  # Invalid date format, retry
            
            elif field == "Passport_No":
                if re.fullmatch(r"[A-Z]{2}\d{7}", text):
                    break
                else:
                    not_verify_number = 1
                    print(f"[WARNING] Passport number '{text}' did not match [A-Z]{{2}}\\d+")

            # No validation needed for other fields
            else:
                break

            print(f"[RETRY] OCR failed validation for {field}: '{text}'")
            retries -= 1



        # Final fallback after retries
        if retries == 0:
            print(f"[ERROR] Final OCR result for {field} still invalid: '{text}'")
            globals.accept = 0

        ocr_results[field] = text

        # Save signature crop
        if field == "Signature":
            signature_path = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_files\signature.png"
            cv2.imwrite(signature_path, cropped)
        
    # Write to a text file
    output_path = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_files\extracted_passport_data.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        for key, value in ocr_results.items():
            f.write(f"{key}: {value}\n")

    print(f"Extraction complete. Text saved to {output_path}")

    # Read extracted data
    file_path = output_path
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                passport_data[key] = value.replace(',', '').replace(':', '')

    # --- Empty field check ---
    globals.accept = 1
    for key, value in passport_data.items():
        if not value.strip():
            print(f"[ERROR] Empty field detected: {key}")
            globals.accept = 0

    # --- Expiry Date check ---
    date_obj = datetime.strptime(passport_data.get("Expiry Date"), "%d-%b-%Y")

    # Get today's date (without time)
    today = datetime.today().date()

    return passport_data

    # Compare
    if date_obj.date() < today:
        globals.accept = 0
        print("Passport Expired\n")