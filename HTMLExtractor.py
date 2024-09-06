import csv

from bs4 import BeautifulSoup

# Open the TXT file containing the HTML content
with open('html_content.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Initialize a list to store extracted data
organization_data = []

# Find all organization tiles
tiles = soup.find_all('div', class_='views-field views-field-nothing')

# Loop over each tile and extract relevant information
for tile in tiles:
    organization = tile.find('h6').text.strip().replace('\xa0', ' ')  # Remove &nbsp;
    category = tile.find('span', class_='color--gray').find('a').text.strip().replace('\xa0', ' ')  # Remove &nbsp;

    # Extract description
    description_tags = tile.find_all('p')
    description = description_tags[1].text.strip().replace('\xa0', ' ') if len(description_tags) > 1 and \
                                                                           description_tags[
                                                                               1].text.strip() else 'NOT FOUND'

    # Extract address (second-to-last <p> tag)
    address = description_tags[-2].text.strip().replace('\xa0', ' ') if len(description_tags) > 2 else 'NOT FOUND'

    # Extract email (last <p> tag)
    contact_info = description_tags[-1].text.strip() if len(description_tags) > 1 else ''

    # Fix: Handle the case where phone is missing but email is present with "| email"
    if '|' in contact_info:
        parts = contact_info.split('|')
        phone = parts[0].strip().replace('\xa0', ' ') if parts[0].strip() else 'NOT FOUND'
        email = parts[1].strip().replace('\xa0', ' ')
    else:
        phone = 'NOT FOUND'
        email = contact_info.strip().replace('\xa0', ' ') if contact_info.startswith('|') else 'NOT FOUND'

    # Safely find the website link and handle the case where the <a> tag is missing
    website_tag = tile.find('a', {'target': '_blank'})
    website = website_tag.get('href', 'NOT FOUND') if website_tag else 'NOT FOUND'

    # Add the extracted data to the list
    organization_data.append({
        'Organization': organization,
        'Category': category,
        'Description': description,
        'Address': address,
        'Phone': phone,  # Leave phone blank if missing
        'Email': email,
        'Website': website
    })

# Write the extracted data to a CSV file
with open('organization_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Organization', 'Category', 'Description', 'Address', 'Phone', 'Email',
                                              'Website'])
    writer.writeheader()
    writer.writerows(organization_data)

print("Data written to 'organization_data.csv'")