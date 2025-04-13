#code used to collect data to train a random forest, to then proceed with its training (INCOMPLETE)

import os
import zipfile
import pandas as pd
from passport import passport_op
from account import account_op
from profile import profile_op
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier  # or Regressor
from sklearn.metrics import classification_report  # or mean_squared_error, etc.

# --- Folder paths ---
folder_bad_hard = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_1701_1900"
folder_bad_easy = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_501_700"
folder_good_easy = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_001_200"
folder_good_hard = r"C:\Users\Client\Python\Programmi\Swiss_Hacks\client_1201_1400"

# --- Helper Functions ---
def extract_all_passports(zip_folder_path, y_label):
    all_passport_data = []
    for file in os.listdir(zip_folder_path):
        if file.endswith('.zip'):
            zip_path = os.path.join(zip_folder_path, file)
            extract_path = os.path.join(zip_folder_path, "temp_extract")
            os.makedirs(extract_path, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            passport_image_path = os.path.join(extract_path, "passport.png")
            if os.path.exists(passport_image_path):
                
                passport_info = passport_op(passport_image_path)

                # Ensure all values are strings, prevent .strip() errors later
                passport_info = {k: str(v).strip() if v is not None else "" for k, v in passport_info.items()}

                passport_info["zip_file"] = file
                passport_info["y"] = y_label
                all_passport_data.append(passport_info)


            else:
                print(f"[WARNING] passport.png not found in {file}")

    return pd.DataFrame(all_passport_data)




def extract_all_accounts(zip_folder_path, y_label):
    all_account_data = []

    for file in os.listdir(zip_folder_path):
        if file.endswith('.zip'):
            zip_path = os.path.join(zip_folder_path, file)
            
            # Use a unique temp folder per zip file
            extract_path = os.path.join(zip_folder_path, f"temp_extract_{os.path.splitext(file)[0]}")
            os.makedirs(extract_path, exist_ok=True)

            # Unzip contents
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)

            account_pdf_path = os.path.join(extract_path, "account.pdf")

            print(extract_path)
            print("-----------------------")
            print(account_pdf_path)

            if os.path.exists(account_pdf_path):
                account_info = account_op(account_pdf_path)

                """if not isinstance(account_info, dict):
                    print(f"[SKIPPED] account_op() returned {type(account_info)} for {zip_path}")
                    continue"""

                account_info["zip_file"] = file
                account_info["y"] = y_label
                all_account_data.append(account_info)

            else:
                print(f"[WARNING] account.pdf not found in {file}")

    return pd.DataFrame(all_account_data)

def extract_all_profiles(zip_folder_path, y_label):
    all_profiles = []
    for file in os.listdir(zip_folder_path):
        if file.endswith(".zip"):
            zip_path = os.path.join(zip_folder_path, file)
            extract_path = os.path.join(zip_folder_path, "temp_extract")
            os.makedirs(extract_path, exist_ok=True)

            try:
                with zipfile.ZipFile(zip_path, "r") as zip_ref:
                    zip_ref.extractall(extract_path)

                profile_info = profile_op(extract_path)
                profile_info["zip_file"] = file
                profile_info["y"] = y_label
                all_profiles.append(profile_info)
            except Exception as e:
                print(f"[ERROR] Failed to process {file}: {e}")

    return pd.DataFrame(all_profiles)

# --- Extract and Combine ---

"""df_passport_good_easy = extract_all_passports(folder_good_easy, y_label=1)
df_passport_bad_easy  = extract_all_passports(folder_bad_easy,  y_label=0)
df_passport_good_hard = extract_all_passports(folder_good_hard, y_label=1)
df_passport_bad_hard  = extract_all_passports(folder_bad_hard,  y_label=0)

df_passports = pd.concat([
    df_passport_good_easy, df_passport_bad_easy,
    df_passport_good_hard, df_passport_bad_hard
], ignore_index=True)
df_passports.to_csv("combined_passport_dataset.csv", index=False)
print("Passports:")
print(df_passports.head())"""


df_account_good_easy = extract_all_accounts(folder_good_easy, y_label=1)
df_account_bad_easy  = extract_all_accounts(folder_bad_easy,  y_label=0)
df_account_good_hard = extract_all_accounts(folder_good_hard, y_label=1)
df_account_bad_hard  = extract_all_accounts(folder_bad_hard,  y_label=0)

df_accounts = pd.concat([
    df_account_good_easy, df_account_bad_easy,
    df_account_good_hard, df_account_bad_hard
], ignore_index=True)
df_accounts.to_csv("combined_account_data.csv", index=False)
print("Accounts:")
print(df_accounts.head())


"""df_profile_good_easy = extract_all_profiles(folder_good_easy, y_label=1)
df_profile_bad_easy  = extract_all_profiles(folder_bad_easy,  y_label=0)
df_profile_good_hard = extract_all_profiles(folder_good_hard, y_label=1)
df_profile_bad_hard  = extract_all_profiles(folder_bad_hard,  y_label=0)

df_profiles = pd.concat([
    df_profile_good_easy, df_profile_bad_easy,
    df_profile_good_hard, df_profile_bad_hard
], ignore_index=True)
df_profiles.to_csv("combined_profile_data.csv", index=False)
print("Profiles:")
print(df_profiles.head())

# --- Optional: Merge all datasets ---
df_merged = df_profiles.merge(df_accounts, on=['zip_file', 'y'], how='inner')
df_merged = df_merged.merge(df_passports, on=['zip_file', 'y'], how='inner')
df_merged.to_csv("final_merged_dataset.csv", index=False)
print("Final merged dataset:")
print(df_merged.head())"""


"""folder_path = "path/to/your/csv/folder"  # e.g., "C:/Users/matte/Desktop/SwissNigg/data"

all_dataframes = []

for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        full_path = os.path.join(folder_path, filename)
        df = pd.read_csv(full_path)
        all_dataframes.append(df)

# Combine all into one DataFrame
full_df = pd.concat(all_dataframes, ignore_index=True)

print(full_df.head())
print(full_df.info())       # Check for nulls, types
print(full_df.isnull().sum())  # See if anything needs to be filled or dropped

X = full_df.drop("label", axis=1)
y = full_df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save dataframe
full_df.to_csv("combined_dataset.csv", index=False)

# Save model using joblib
import joblib
joblib.dump(clf, "random_forest_model.pkl")"""
