import re
from fuzzywuzzy import fuzz

def custom_similarity(name1, name2):
    full_ratio = fuzz.ratio(name1, name2)
    partial_ratio = fuzz.partial_ratio(name1, name2)
    token_sort_ratio = fuzz.token_sort_ratio(name1, name2)
    
    return (full_ratio + partial_ratio + token_sort_ratio) / 3

no_names_file = '/Users/akshansh.pandey/Downloads/no_names.txt'
all_email_file = '/Users/akshansh.pandey/Downloads/allEmail.txt'

# Read and clean names from file
with open(no_names_file, 'r') as file:
    no_names = file.read().splitlines()

with open(all_email_file, 'r') as file:
    all_emails = file.read().splitlines()

cleaned_no_names = []
for name in no_names:
    name = name.split('<')[0]
    cleaned_name = name.strip().lower()
    cleaned_no_names.append(cleaned_name)

# Regex pattern to extract full name and email
pattern = re.compile(r'fullName":"([^"]+)","email":"([^"]+)')

name_email_dict = {}

# print(all_emails)
# Process each cleaned name against all email entries
for cleaned_name in cleaned_no_names:
    best_score = 0
    best_match = None
    
    # Iterate through all email entries only if cleaned_name is in all_emails
    for email_entry in all_emails:
        match = pattern.search(email_entry)
        if match:
            full_name = match.group(1).strip().lower()
            email = match.group(2).strip()
            
            similarity_score = custom_similarity(full_name, cleaned_name)
            
            if similarity_score > 60:  # Similarity threshold
                if similarity_score > best_score:
                    best_score = similarity_score
                    name_email_dict[cleaned_name] = email
    

# Output results
for name in cleaned_no_names:
    if name in name_email_dict:
        print(f"{name.title()} : {name_email_dict[name]}")
    else:
        print(f"{name.title()} : Not Found")




name1 = "Sesha Gagan Tipparaju".strip().lower()
name2 = "Tipparaju Sesha Gagan".strip().lower()
similarity_score = custom_similarity(name1, name2)
print(f"Similarity score between '{name1}' and '{name2}': {similarity_score}")
