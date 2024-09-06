# Read the text file with correct encoding (utf-8)
with open('FinalList.txt', 'r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()  # Read all lines

# Print the first 50 lines to inspect the structure
for i, line in enumerate(lines[:50], 1):
    print(f"{i}: {line.strip()}")