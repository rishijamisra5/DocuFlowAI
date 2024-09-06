import re
import pandas as pd

# Regular expression to match email addresses
email_re = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

# Regular expression to detect a website (any line with a dot but not an email)
def is_website(line):
    return '.' in line and not email_re.search(line)

def extract_data_from_untagged(lines):
    data_list = []
    current_entry = {}
    field_count = 0  # Track which field we're currently processing

    for line in lines:
        line = line.strip().rstrip('/')  # Strip trailing slashes and whitespace

        # Skip blank lines (signifying the space between fields)
        if not line:
            # If we expect a description but find a blank line, mark it as 'NOT FOUND'
            if field_count == 2:
                current_entry['Description'] = 'NOT FOUND'
                field_count += 1
            continue

        # Organization (1st field)
        if field_count == 0:
            current_entry['Organization'] = line
            field_count += 1

        # Category (2nd field)
        elif field_count == 1:
            current_entry['Category'] = line
            field_count += 1

        # Description (3rd field, if not provided, it's considered as 'NOT FOUND')
        elif field_count == 2:
            if not is_website(line) and '|' not in line:
                current_entry['Description'] = line if line != '.' else 'NOT FOUND'
                field_count += 1
            else:
                current_entry['Description'] = 'NOT FOUND'
                field_count += 1

        # Address (4th field)
        elif field_count == 3:
            current_entry['Address'] = line
            field_count += 1

        # Phone Number (5th field) and Email (6th field)
        elif field_count == 4:
            if '|' in line:  # If phone and email are on the same line
                parts = line.split('|', 1)
                current_entry['Phone'] = parts[0].strip() if parts[0].strip() else 'NOT FOUND'
                current_entry['Email'] = parts[1].strip() if parts[1].strip() else 'NOT FOUND'
            else:  # Only email or phone is present
                current_entry['Phone'] = 'NOT FOUND'
                current_entry['Email'] = email_re.search(line).group() if email_re.search(line) else 'NOT FOUND'
            field_count += 1

        # Website (7th field, handle "NA" as 'NOT FOUND')
        elif field_count == 5 and (is_website(line) or line == 'NA'):
            current_entry['Website'] = 'NOT FOUND' if line == 'NA' else line
            field_count += 1

        # If all fields have been processed, append the entry and reset
        if field_count == 6:
            # Ensure missing fields are set to 'NOT FOUND'
            current_entry.setdefault('Description', 'NOT FOUND')
            current_entry.setdefault('Website', 'NOT FOUND')
            current_entry.setdefault('Phone', 'NOT FOUND')
            current_entry.setdefault('Email', 'NOT FOUND')
            data_list.append(current_entry)
            current_entry = {}
            field_count = 0  # Reset for the next entry

    # Append the last entry if it exists
    if current_entry:
        # Ensure missing fields are set to 'NOT FOUND' for the last entry
        current_entry.setdefault('Description', 'NOT FOUND')
        current_entry.setdefault('Website', 'NOT FOUND')
        current_entry.setdefault('Phone', 'NOT FOUND')
        current_entry.setdefault('Email', 'NOT FOUND')
        data_list.append(current_entry)

    return data_list

# Read the text file with correct encoding (utf-8)
with open('FinalListNewFormat.txt', 'r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()  # Read all lines

# Extract data from each entry
data_list = extract_data_from_untagged(lines)

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data_list)

# Display the DataFrame
print(df)

# Optionally save to CSV
df.to_csv('extracted_data_new_format.csv', index=False)
