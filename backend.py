#Main file that plays the backend of the game, and compares between different files



import requests
import base64
import os
import globals
from unidecode import unidecode
from docx import Document
import re
import pandas as pd

from passport import passport_op
from account import account_op
from passport import passport_data
from account import account_data
from profile import profile_op
from profile import profile

from passport import not_verify_number, not_verify_name

def normalize_string(s):
    return unidecode(s).lower()

es_gehet = 1
copy_data = "ciao"

keys = {
   "GivenNames",
    "Surname",
    "Passport_No",
    "country",
    "phone_number",
    "email"
}

# === CONFIGURATION ===
api_key = "VgNcmM6Z1bZVjMxBYjBnf3n9VxMbMI6f9rQiU4mgAUs"
team_name = "Bayers Bros"

# === API ENDPOINTS ===
start_url = "https://hackathon-api.mlo.sehlat.io/game/start"
client_url = "https://hackathon-api.mlo.sehlat.io/game/client"
request_url = "https://hackathon-api.mlo.sehlat.io/game/decision"
headers = {
    "x-api-key": api_key,
    "Content-Type": "application/json"
}

# === STEP 1: Start the game ===
start_payload = {"player_name": team_name}
start_response = requests.post(start_url, headers=headers, json=start_payload)

if start_response.ok:
    print("✅ Game started successfully.")
else:
    print("❌ Failed to start game.")
    print("Status code:", start_response.status_code)
    print("Response:", start_response.text)
    exit(1)

client_data = start_response.json()
session_id = client_data["session_id"]

while(es_gehet):

    # Decode and save files ===
    os.makedirs("client_files", exist_ok=True)

    def save_base64_file(data, path):
        with open(path, "wb") as f:
            f.write(base64.b64decode(data))

    # ✅ Access nested client_data
    client_files = client_data["client_data"]

    save_base64_file(client_files["passport"], "client_files/passport.png")
    save_base64_file(client_files["description"], "client_files/description.txt")
    save_base64_file(client_files["profile"], "client_files/profile.docx")
    save_base64_file(client_files["account"], "client_files/account.pdf")

    passport_op(r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_files\passport.png")
    print("passport operation successful")

    account_op(r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_files\account.pdf")
    print("account operation successful")

    profile_op(r'C:\Users\Client\Python\Programmi\Swiss_Hacks\client_files\profile.docx')
    print("profile operation successful")

    if globals.accept == 1:
        from passport import not_verify_number, not_verify_name
        for k in keys:
            # 1) Skip if there's a passport number error and k == "Passport_No"
            if k == "Passport_No" and not_verify_number == 1:
                print("skipping number verification")
                continue

            # 2) Skip if there's a name error and k is either "Surname" or "GivenNames"
            if (k == "Surname" or k == "GivenNames") and not_verify_name == 1:
                print("skipping name verification")
                continue

            # ----- Perform checks only if we're not skipping -----

            # Check if the field is in both account_data and passport_data
            if k in account_data and k in passport_data:
                if re.fullmatch(r"[A-Z]{2}\d{7}", normalize_string(passport_data[k])):
                    globals.accept = (normalize_string(account_data[k]) == normalize_string(passport_data[k]))
                    if globals.accept == 0:
                        print(normalize_string(account_data[k]))
                        print("---------")
                        print(normalize_string(passport_data[k]))
                        print("\n")

            # Check if the field is in both account_data and profile
            if k in account_data and k in profile:
                globals.accept = (normalize_string(account_data[k]) == normalize_string(profile[k]))
                if globals.accept == 0:
                    print(normalize_string(account_data[k]))
                    print("---------")
                    print(normalize_string(profile[k]))
                    print("\n")
                

    #if globals.accept:
        #TRY WITH DECISION TREES

            
    if globals.accept:
        answer = {
        "decision": "Accept",
        "session_id": session_id,
        "client_id": client_data["client_id"]
        }
        print("ACCEPTED")
    else:
        answer = {
        "decision": "Reject",
        "session_id": session_id,
        "client_id": client_data["client_id"]
        }
        print("REJECTED")

    #Send response and get new client
    response = requests.post(request_url, headers = headers, json = answer)

    client_data = response.json()

    if(client_data["status"] == "gameover"):
        es_gehet = 0
        print(client_data["score"])

    
            