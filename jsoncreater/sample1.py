import json
import re

content_array = []
words  = []
words1  = []
content_array1 = []
search_string='E-Mail'
search_string2='Bank Details'
search_string1='Bank Details'
with open("../pdf/B1.json") as f:
                #Content_list is the list that contains the read lines.     
                for line in f:
                        if search_string in line:                        
                           words1 = line.split('\\n')
                        if search_string1 in line:   
                           words = line.split('\\n')                              
                       
                             #content_array.append(line)print(content_array)

for item1 in words1:
  print(item1)   
for item in words:
  print(item)                
# Load JSON file
with open('C:\Allfiles\B1.json', 'r') as f:
    data = json.load(f)

# Initialize result dictionary
key_value_pairs = {}                #Content_list is the list that contains the read lines.     

# Access the table
tables = data[0]['tables'][0]  # first page, first tabl

# Extract key-value pairs from the 5th column (index 4)
for row in tables:
    if len(row) > 4 and row[4]:
        cell = row[4]
        # If cell contains newline, assume it's key and value
        if '\n' in cell:
            parts = cell.split('\n', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            key_value_pairs[key] = value
        else:
            # If it's a lone key without value, assign empty string
            key_value_pairs[cell.strip()] = ""


tables1 = data[0]['tables'][0]  # first page, first tabl


# Print the result
print(json.dumps(key_value_pairs, indent=4))