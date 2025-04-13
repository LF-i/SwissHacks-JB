#This script collects the data from the profile Word document, structures it and cleans it taking care of all 
#the exceptions. Then it performs a series of tailored checks.

# Modify the loop in Cell 1 to handle the "Communication Medium" table
import os
import zipfile
from docx import Document
import re
import globals

profile = {}

def profile_op(doc_path):

    # List to store the dictionaries for all "profile.docx" files
    person_data = {}
    
    with open('client_files\description.txt', 'r', encoding='utf-8') as txt_file:
        description_content = txt_file.read().strip()
        person_data['Description'] = description_content

    if os.path.exists(doc_path):
        # Read the .docx file
        doc = Document(doc_path)
        # Extract table data
        check_employment_and_function = False

        for table in doc.tables:

            # Check if the table is the "Communication Medium" table
            if table.rows[0].cells[0].text.strip() == "Communication Medium":
                for row in table.rows:
                    if len(row.cells) > 1 and row.cells[2].text.strip():
                        # Split the second cell into key and value
                        right_column = row.cells[2].text.strip()
                        parts = right_column.split(maxsplit=1)
                        if len(parts) == 2:
                            key = parts[0]  # First word as key
                            value = parts[1]  # Remaining text as value
                            person_data[key] = value
            # Check if the table is the "Current employment and function" table
            elif table.rows[0].cells[0].text.strip() == "Current employment and function":

                check_employment_and_function = True

                employed_status, since_emp, name_employer, position = 'No', '', '', ''
                self_employed_status, since_self_emp, name_employer, position = 'No', '', '', ''

                for row in table.rows:
                    row_text = row.cells[2].text.strip()

                    if "☒  Employee" in row_text:
                        employed_status = "Yes"
                        since_emp = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""                                                
                    elif "Name Employer" in row_text:
                        name_employer = row_text.split("Name Employer")[1].strip()
                    elif "Position" in row_text:
                        position = row_text.split("Position")[1].strip()
                    elif '☒ Self-Employed' in row_text:
                        self_employed_status = "Yes"
                        since_self_emp = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""                                                
                    elif "Company Name" in row_text:
                        company_name = row_text.split("Company Name")[1].strip()
                    elif r"% of ownership" in row_text:
                        perc_of_ownership = row_text.split(r"% of ownership")[1].strip()

                person_data["Employed"] = [employed_status, since_emp, name_employer, position]
                person_data["Self-Employed"] = [self_employed_status, since_self_emp, company_name, perc_of_ownership]

            elif check_employment_and_function:

                currently_not_employed_check = False
                retired_check = False
                retired_home_check = False
                student_check = False
                diplomat_check = False
                military_check = False
                other_check = False

                currently_not_employed, since_not_empl, prev_prof_1 = 'No', '', ''
                retired, since_retired, prev_prof_2 = 'No', '', ''
                house, since_home, prev_prof_3 = 'No', '', ''
                student, since_student, country_of_study, prev_prof_4 = 'No', '', '', ''
                diplomat, since_diplomat, dimpl_country, prev_prof_5 = 'No', '', '', ''
                militar, since_military, military_country, prev_prof_6 = 'No', '', '', ''
                other, what_other, since_other, prev_prof_7 = 'No', '', '', ''
                unknown, unknown_content = 'No', ''

                for row in table.rows:
                    row_text = row.cells[2].text.strip()

                    if "☒ Currently not employed" in row_text:
                        currently_not_employed = 'Yes'
                        since_not_empl = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        currently_not_employed_check = True
                    elif "Previous Profession:" in row_text and currently_not_employed_check:
                        prev_prof_1 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        currently_not_employed_check = False

                    if "☒ Retired" in row_text:
                        retired = 'Yes'
                        since_retired = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        retired_check = True
                    elif "Previous Profession:" in row_text and retired_check:
                        prev_prof_2 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        retired_check = False

                    if "☒ Homemaker/housewife" in row_text:
                        house = 'Yes'
                        since_home = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        retired_home_check = True
                    elif "Previous Profession:" in row_text and retired_home_check:
                        prev_prof_3 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        retired_home_check = False

                    if "☒ Student" in row_text:
                        student = 'Yes'
                        since_student = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        country_of_study = row_text.split("Country of study:")[1] if "Country of study:" in row_text else ""
                        student_check = True
                    elif "Previous Profession:" in row_text and student_check:
                        prev_prof_4 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        student_check = False

                    if "☒ Diplomat" in row_text:
                        diplomat = 'Yes'
                        since_diplomat = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        dimpl_country = row_text.split("Home country of diplomatic mission:")[1] if "Home country of diplomatic mission:" in row_text else ""
                        diplomat_check = True
                    elif "Previous Profession:" in row_text and diplomat_check:
                        prev_prof_5 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        diplomat_check = False

                    if "☒ Military representative" in row_text:
                        militar = 'Yes'
                        since_military = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        military_country = row_text.split("Home country of military establishment:")[1] if "Home country of military establishment:" in row_text else ""
                        military_check = True
                    elif "Previous Profession:" in row_text and military_check:
                        prev_prof_6 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        military_check = False

                    if "☒ Other" in row_text:
                        other = 'Yes'
                        since_other = row_text.split("Since")[1].split()[0] if "Since" in row_text else ""
                        what_other = row_text.split("Other")[1].split()[0] if "Other" in row_text else ""
                        other_check = True
                    elif "Previous Profession:" in row_text and other_check:
                        prev_prof_7 = row_text.split("Previous Profession:")[1] if "Previous Profession:" in row_text else ""
                        other_check = False

                    if "☒ Unknown" in row_text:
                        unknown = 'Yes'
                        unknown_content = row_text.split("Unknown")[1]

                person_data["Currently Not Employed"] = [currently_not_employed, since_not_empl, prev_prof_1]
                person_data["Retired"] = [retired, since_retired, prev_prof_2]
                person_data["Homemaker/housewife"] = [house, since_home, prev_prof_3]
                person_data["Student"] = [student, since_student, country_of_study, prev_prof_4]
                person_data["Diplomat"] = [diplomat, since_diplomat, dimpl_country, prev_prof_5]
                person_data["Militar"] = [militar, since_military, military_country, prev_prof_6]
                person_data["Other"] = [other, what_other, since_other, prev_prof_7]
                person_data["Unknown"] = [unknown, unknown_content]

                check_employment_and_function = False

            if table.rows[0].cells[0].text.strip() == "Total wealth estimated":

                for row in table.rows:
                    
                    row_text = row.cells[2].text.strip()
                    parts = [p.strip() for p in row_text.split(',')]

                    if len(parts) == 3:

                        person_data["Origin of wealth (TEXT)"] = parts

                    else:

                        cells = [cell.text.strip() for cell in row.cells]
                        if len(cells) >= 2 and cells[0]:  # Ensure the row has a key and value
                            key = cells[0]
                            value = ' '.join(cells[1:]).strip()
                            person_data[key] = value

            else:
                # Process other tables as usual
                for row in table.rows:
                    cells = [cell.text.strip() for cell in row.cells]
                    if len(cells) >= 2 and cells[0]:  # Ensure the row has a key and value
                        key = cells[0]
                        value = ' '.join(cells[1:]).strip()
                        person_data[key] = value

            last_table = table

            # Append the person's data dictionary to the profiles list
            profile = person_data
    else:
        globals.accept = 0

    # Function to process values containing multiple ☒ elements
    def extract_checked_value(value):
        if '☒' in value:
            results = []
            parts = value.split('☒')  # Split the value by each occurrence of ☒
            for part in parts[1:]:  # Skip the first part (before the first ☒)
                if '☐' in part:  # Check if there is a subsequent ☐
                    results.append(part.split('☐', 1)[0].strip())
                elif '☒' in part:  # Check if there is a subsequent ☒
                    results.append(part.split('☒', 1)[0].strip())
                else:  # If no ☐ or ☒ exists, take the entire part
                    results.append(part.strip())
            return results  # Return the list of extracted values
        return None # Return the 0 if no '☒' is found

    # Process all profiles to update values containing multiple ☒ elements
    for key, value in profile.items():
        if '☐' in value or '☒' in value:  # Check if the value contains ☐ or ☒
            profile[key] = extract_checked_value(value)


    # Function to process rows where the key contains both key and values
    def split_key_and_values(key):
        if '☒' in key or '☐' in key:  # Check if the key contains checkboxes
            parts = key.split('\n', 1)  # Split into the first line (key) and the rest (values)
            if len(parts) == 2:
                actual_key = parts[0].strip()  # The first line is the actual key
                values = extract_checked_value(parts[1])  # Process the values using the existing function
                return actual_key, values
        return key, None  # Return the original key and None if no checkboxes are found

    # Update the logic for processing rows in the table

        updated_profile = {}
        for key, value in profile.items():
            # Check if the key contains both key and values
            actual_key, extracted_values = split_key_and_values(key)
            if extracted_values is not None:
                updated_profile[actual_key] = extracted_values  # Use the extracted values
            else:
                updated_profile[actual_key] = value  # Use the original value if no extraction is needed
        profile.clear()
        profile.update(updated_profile)

    def split_address(address):
        # Updated regex to handle various postal code formats and address structures
        match = re.match(r"(.+?)\s+(\d+),\s+([\d\- ]+)\s+(.+)", address)
        if match:
            return {
                "street": match.group(1).strip(),
                "building_number": match.group(2).strip(),
                "postal_code": match.group(3).strip(),
                "city": match.group(4).strip(),
            }
        return None

    import re

    address = profile['Address']
    match = re.match(r"(.+?)\s+(\d+),\s+([\d\- ]+)\s+(.+)", address)

    if match:
        profile['street_name'] = match.group(1).strip()
        profile['building_number'] = match.group(2).strip()
        profile['postal_code'] = match.group(3).strip()
        profile['city'] = match.group(4).strip()


        
    profile['Surname'] = profile.pop('Last Name')
    profile['GivenNames'] = profile.pop('First/ Middle Name (s)')
    profile['Passport_No'] = profile.pop('Passport No/ Unique ID')
    profile['country'] = profile.pop('Country of Domicile')
    #profile['phone_number'] = profile.pop('Telephone')
    profile['email'] = profile.pop('E-Mail')


    import unicodedata
    import re

    def remove_special_letters(text):
        return re.sub(r'[^a-zA-Z\s]', '', text)
    def remove_accents(text):
        return ''.join(
            c for c in unicodedata.normalize('NFD', text)
            if unicodedata.category(c) != 'Mn'
        )

    email = profile['email']
    local_part = email.split('@')[0]
    parts = local_part.split('.')
    if len(parts) == 2:
        profile['first_name_email'] = parts[0].lower()
        profile['last_name_email'] = parts[1].lower()
    else:
        print('error name and last name')


    def extract_year(text):
        match = re.search(r"\((\d{4})\)", text)
        return match.group(1) if match else None

    profile['Education History End Date'] = extract_year(profile['Education History'])


    def extract_salary_info(text):
        match = re.search(r"\((\d+)\s*(\w+)\s*p\.A\.\)", text)
        if match:
            return {
                "amount": int(match.group(1)),
                "currency": match.group(2)
            }
        return {
                "amount": '',
                "currency": ''
            }

    def extract_job_name(text):
        match = re.match(r'^(.?)\s\(', text.strip())
        return match.group(1) if match else text

    job_name = extract_job_name(profile['Employed'][3])
    profile['Employed'].append(job_name)
    salary_info = extract_salary_info(profile['Employed'][3])
    profile['Employed'].append(salary_info['amount'])
    profile['Employed'].append(salary_info['currency'])


    import requests

    def get_gender(name):
        url = f"https://api.genderize.io?name={name}"
        response = requests.get(url)
        data = response.json()
        
        if data.get("gender"):
            return data["gender"]
        else:
            return "Unknown"


    profile['GivenNamesGender'] = get_gender(profile['GivenNames'])
    profile['GivenNamesGender'] = profile['GivenNamesGender'].lower()
    profile['Gender'] = profile['Gender'][0].lower()


    total_sum = 0

    if profile['Estimated Assets']:
        # Iterate through the list and extract numeric values
        for item in profile['Estimated Assets']:
            # Split the string by tab characters
            parts = item.split('\t')
            
            # Extract the numeric value (last part of the string)
            value = parts[2]
            
            # Add the numeric value to the total sum
            total_sum += int(value)

    profile['Estimated Assets Sum'] = total_sum

    ### FIX EDU
    # print(profile['Education History'].split(','))
    profile['Education History'] = profile['Education History'].split(',')

    for i, edu in enumerate(profile['Education History']):
        profile['Education History'][i] = edu[:-7]


    #-------------------------RULES CHECK STARTS HERE--------------------

    ### Estimated Assets Sum < Total Asset Under Management


    ok = int(profile['Estimated Assets Sum']) <= int(profile['Total Asset Under Management'])

    if not ok:
        print(profile['Estimated Assets Sum'], ':', profile['Total Asset Under Management'])
        globals.accept = 0


    ### Date of birth < ID Issue Date

    ok = profile['Date of birth'] <= profile['ID Issue Date']

    if not ok:
        print(profile['Date of birth'], ':', profile['ID Issue Date'])
        globals.accept = 0


    ### Date of birth < Education History End Date

    import pandas as pd
            
    if profile['Education History End Date']:

        ok = pd.to_datetime(profile['Date of birth']) < pd.to_datetime(profile['Education History End Date'])

    else:
        ok = True

    if not ok:
        print(profile['Date of birth'], ':', profile['Education History End Date'])
        globals.accept = 0


    ### ID Issue Date < ID Expiry Date

    ok = profile['ID Issue Date'] < profile['ID Expiry Date']

    if not ok:
        print(profile['ID Issue Date'], ':', profile['ID Expiry Date'])
        globals.accept = 0

    ### Check: email surname corresponds to surname

    errors = 0

    #surname_email = remove_special_letters(remove_accents(profile["last_name_email"].replace(" ", "").lower())) 
    surname = remove_special_letters(remove_accents(profile["Surname"].replace(" ", "").lower()))

    #ok = surname_email == surname

    #if not ok:
     #   print(surname ,':', surname_email)
      #  globals.accept = 0


    ### Check: name gender corresponds to gender

    if profile['GivenNamesGender'] != 'unknown':
        ok = profile['GivenNamesGender'] == profile['Gender']
    else:
        ok = True

    if not ok:
        print(profile['Gender'], ':', profile['GivenNamesGender'])
        globals.accept = 0
        

    ### Check: Education History End Date < Emploment Start Date

    edu_end_date = profile['Education History End Date']
    empl_start_date = profile['Employed'][1]

    if edu_end_date and empl_start_date:
        ok = int(edu_end_date) <= int(empl_start_date)
    else:
        ok = True

    if not ok:
        print(profile['Education History End Date'], ':', profile['Employed'])
        globals.accept = 0


    tertiary_edus = []

    if profile['Highest education attained'] == 'Tertiary':

        tertiary_edus.append(profile['Education History'])


    ### Highest education attained == 'Tertiary' and university keywords in Education History

    def is_probable_university_entry(text):
        return bool(re.search(r'\b(university|college|institute|school of)\b', text.lower()))

    def contains_any_word(word_list, multi_word_string):
        for word in word_list:
            if word.lower() in multi_word_string.lower():
                return True
        return False

    university_keywords = [
        'University', 'School', 'Business', 'Universidad',
        'Polytechnic', 'Institute', 'Academy', 'Université', 'College',
        'KU', 'Instituut', 'EMIC', 'HEC', 'EPFL', 'IUT',
        'Universiteit', 'ENS', 'Hochschule', 'Fachhochschule', 'Technik',
        'Faculty', 'Graduate School', 'Open University', 'Education Centre',
        'UCL', 'MIT', 'Caltech', 'SU', 'NTU', 'NUS', 'HKU', 'UNAM',
        'Technische Universität', 'Universität', 'Grande École', 'École',
        'CentraleSupélec', 'Pontificia', 'Tecnológico', 'Escuela',
        'Politecnico', 'Scuola Superiore', 'Università', 'Hogeschool',
        'Faculdade', 'Centro Universitário', 'Academy of Sciences',
        'Tsinghua', 'Peking University', 'State University',
        'Technical University', 'Moscow Institute', 'Berufsakademie'
    ]

    highest_edu_attained = profile['Highest education attained']
    edu_history = profile['Education History'][:-7] # profile['Education History']

    if highest_edu_attained == 'Tertiary':

        for edu in edu_history:
            if contains_any_word(university_keywords, edu) or is_probable_university_entry(edu_history):
                ok = True
            else:
                ok = False
                print(edu_history)

    today = pd.Timestamp.today().normalize()
    #check expiration date
    if pd.to_datetime(profile['ID Expiry Date']) < today:
        globals.accept = 0

    """if not contains_any_word(profiles[0]['GivenNames'], profiles[0]['Description']):
        ok = False
        print('Different GivenNames!')
        globals.accept = 0
    if not contains_any_word(profiles[0]['Surname'], profiles[0]['Description']):
        ok = False
        print('Different Surname!')
        globals.accept = 0
    if not contains_any_word(profiles[0]['Marital Status'][0].split()[0], profiles[0]['Description']):
        ok = False
        print('Different Marital Status!')
        globals.accept = 0"""

    def contains_word(word, multi_word_string):
        if word.lower() in multi_word_string.lower():
            return True
        return False

    if not contains_word(profile['GivenNames'], profile['Description']):
        ok = False
        print('Different GivenNames!')
        globals.accept = 0
    if not contains_word(profile['Surname'], profile['Description']):
        ok = False
        print('Different Surname!')
        globals.accept = 0

    if profile['Marital Status'][0].split()[0] == 'Married':

        if not contains_any_word(['Married','tied the knot'], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Marital Status!')

    if profile['Marital Status'][0].split()[0] in ['Divorced','Widowed','Single']:

        if not contains_word(profile['Marital Status'][0].split()[0], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Marital Status!')

    if not contains_any_word(profile['Education History'], profile['Description']):
        ok = False
        globals.accept = 0
        print('Different Education!')

    if profile['Education History End Date']:
        if not contains_word(profile['Education History End Date'], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Education History End Date!')

    if profile['Employed'][0] == 'Yes':
        if not contains_word(profile['Employed'][2], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Employer!')

        """if not contains_word(profile['Employed'][4], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Profession!')"""

        if not contains_word(str(profile['Employed'][5]), profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Salary!')

        if not contains_word(str(profile['Employed'][6]), profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Salary Currency!')

    if profile['Retired'][0] == 'Yes':
        if not contains_word(profile['Retired'][2], profile['Description']):
            ok = False
            globals.accept = 0
            print('Different Previous Profession!')

