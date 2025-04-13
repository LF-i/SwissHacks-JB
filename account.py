#Code that reads data from the account file, performs basic checks and structures it into a Python dictionary


import PyPDF2
import fitz
import re
import globals

account_data = {}
# -------------------------------
# Fase 1: Lettura ed estrazione dal PDF (reader)
# -------------------------------
def estrai_dati_campi_modulo(percorso_pdf: str) -> dict:
    """
    Estrae i valori dei campi modulo (form fields) da un PDF.
    Restituisce un dizionario con {nome_campo: valore}.
    Se il PDF non contiene campi modulo, restituisce un dizionario vuoto.
    Inoltre estrae una porzione della prima pagina per salvare la firma.
    """
    dati_estratti = {}
    try:
        with open(percorso_pdf, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            # get_fields() restituisce un dizionario con tutti i campi modulo
            fields = reader.get_fields()
            if fields:
                for nome_campo, attributi_campo in fields.items():
                    # Il valore del campo si trova solitamente in attributi_campo["/V"]
                    valore = attributi_campo.get("/V")
                    if valore is None:
                        valore = ""
                    dati_estratti[nome_campo] = valore
    except Exception as e:
        print(f"Errore durante la lettura del PDF: {e}")

    # Esempio: estrazione della firma dalla prima pagina
    try:
        doc = fitz.open(percorso_pdf)
        page = doc[0]  # supponendo che la firma sia in prima pagina
        # Specifica l'area da ritagliare (modifica le coordinate se necessario)
        firma_rect = fitz.Rect(80, 585, 210, 615)  # x0, y0, x1, y1
        mat = fitz.Matrix(2, 2)  # ingrandimento del rendering
        pix = page.get_pixmap(matrix=mat, clip=firma_rect)
        pix.save("firma_rasterizzata.png")
        doc.close()
    except Exception as e:
        print(f"Errore durante l'estrazione della firma: {e}")

    return dati_estratti

def scrivi_risultati_su_file(dati: dict, file_output: str):
    """
    Scrive il dizionario di dati sul file di testo.
    """
    try:
        with open(file_output, "w", encoding="utf-8") as f:
            for chiave, valore in dati.items():
                print(f"{chiave}: {valore}", file=f)
    except Exception as e:
        print(f"Errore durante la scrittura su file: {e}")

# -------------------------------
# Fase 2: Validazione dei dati (controllo)
# -------------------------------
def is_valid_email(email: str) -> bool:
    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    return bool(re.match(pattern, email.strip()))

def is_valid_phone(phone: str) -> bool:
    """
    Controllo semplice per numero di telefono:
    - Può iniziare con un + (opzionale)
    - Può contenere solo cifre e spazi (oltre all'eventuale + iniziale)
    - Deve avere almeno 7 cifre (escludendo gli spazi)
    """
    phone = phone.strip()
    pattern = r'^(?=(?:.*\d){7,})\+?[0-9 ]+$'
    return bool(re.match(pattern, phone))

def valida_dati_cliente(dati: dict) -> tuple[bool, list]:
    """
    Controlla che:
      - "account_name" sia uguale a account_holder_name + " " + account_holder_surname
      - "name" sia uguale a account_holder_name + " " + account_holder_surname
      - "email" e "phone_number" siano in un formato valido
    Restituisce (True, []) se tutto è OK oppure (False, [lista errori]) in caso di problemi.
    """
    is_valid = True
    errori = []

    required_keys = [
        "account_name",
        "account_holder_name",
        "account_holder_surname",
        "name",
        "phone_number",
        "email",
        "street_name",
        "country",
        "city",
        "postal_code",
        "building_number",
        "passport_number",
    ]
    # Verifica che i campi minimi siano presenti
    for k in required_keys:
        if not dati[k]:
            errori.append(f"Manca il campo: {k}")
            is_valid = False

    if is_valid:  # Procedi con i controlli solo se le chiavi sono presenti
        expected_full_name = f"{dati['account_holder_name']} {dati['account_holder_surname']}"
        if dati["account_name"] != expected_full_name:
            is_valid = False
            globals.accept = 0
            errori.append(f"account_name '{dati['account_name']}' != '{expected_full_name}'")
        if dati["name"] != expected_full_name:
            is_valid = False
            globals.accept = 0
            errori.append(f"name '{dati['name']}' != '{expected_full_name}'")
        if not is_valid_email(dati["email"]):
            is_valid = False
            globals.accept = 0
            errori.append(f"Email '{dati['email']}' non è valida.")
        if not is_valid_phone(dati["phone_number"]):
            is_valid = False
            globals.accept = 0
            errori.append(f"Numero di telefono '{dati['phone_number']}' non è valido.")
        if dati["chf"] == "/Off" and dati["eur"] == "/Off" and dati["usd"] == "/Off" and "other_ccy" not in dati:
            is_valid = False
            globals.accept = 0
            errori.append(f"Currency not inserted\n")
    else:
        globals.accept = 0

    return (is_valid, errori)

def leggi_dati_da_file(file_txt: str) -> dict:
    """
    Legge un file di testo con righe "chiave: valore" e restituisce un dizionario.
    """
    dati_estratti = {}
    try:
        with open(file_txt, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":", 1)
                if len(parts) == 2:
                    chiave = parts[0].strip()
                    valore = parts[1].strip()
                    dati_estratti[chiave] = valore
    except Exception as e:
        print(f"Errore durante la lettura del file {file_txt}: {e}")
    return dati_estratti

# -------------------------------
# Fase 3: Rinominazione delle chiavi (dizionario)
# -------------------------------
def leggi_e_rinomina(file_txt: str, mapping: dict) -> dict:
    """
    Legge un file "chiave: valore" e rinomina le chiavi secondo il dizionario di mapping.
    Se una chiave non è presente nel mapping, la mantiene invariata.
    """
    try:
        with open(file_txt, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":", 1)
                if len(parts) == 2:
                    old_key = parts[0].strip()
                    valore = parts[1].strip()
                    new_key = mapping.get(old_key, old_key)
                    account_data[new_key] = valore
                else:
                    print(f"Riga non valida o senza ':': {line}")
    except Exception as e:
        print(f"Errore durante la lettura per il dizionario: {e}")
    return account_data

# -------------------------------
# Programma principale unificato
# -------------------------------
def account_op(pdf_path):
    # Definisci il percorso del PDF (modifica in base al tuo ambiente)
    file_output = "risultati.txt"

    print("Avvio fase di estrazione dati dal PDF...")
    dati_estratti = estrai_dati_campi_modulo(pdf_path)
    if not dati_estratti:
        print("Nessun campo estratto dal PDF!")
    else:
        print("Scrittura dei risultati su file...")
        scrivi_risultati_su_file(dati_estratti, file_output)

        # Fase di controllo/validazione
        print("\nAvvio fase di validazione dei dati...")
        dati_letti = leggi_dati_da_file(file_output)
        validi, errori = valida_dati_cliente(dati_letti)
        if validi:
            print("Tutti i campi sono validi.")
        else:
            print("Sono stati rilevati dei problemi:")
            for err in errori:
                print(" -", err)

        # Fase di rinominazione delle chiavi (dizionario)
        print("\nAvvio fase di rinominazione delle chiavi...")
        KEYS_MAPPING = {
            "account_name": "name_surname",
            "account_holder_name": "GivenNames",
            "account_holder_surname": "Surname",
            "passport_number": "Passport_No"
        }
        nuovo_diz = leggi_e_rinomina(file_output, KEYS_MAPPING)
        
        return account_data

if __name__ == "__main__":
    main()