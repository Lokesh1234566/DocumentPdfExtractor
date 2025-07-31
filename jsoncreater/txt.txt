import json
import re

# Load JSON
with open('../pdf/A1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

result = {}

# Get the first cell of the first table
header_block = data[0]['tables'][0][0][0]

# Split into lines
lines = header_block.split('\n')

def extract_key_value_from_line(line):
    if ':' in line:
        key, value = line.split(':', 1)
        return key.strip(), value.strip()
    elif ' : ' in line:
        key, value = line.split(' : ', 1)
        return key.strip(), value.strip()
    return None, None

# Parse header block
company_lines = []
buyer_lines = []
is_buyer = False
for line in lines:
    if line.strip() == "Buyer":
        is_buyer = True
        continue
    if is_buyer:
        buyer_lines.append(line.strip())
    else:
        company_lines.append(line.strip())

# Parse company info
for line in company_lines:
    key, value = extract_key_value_from_line(line)
    if key and value:
        result[key] = value
    elif line:
        result.setdefault("Company Info", []).append(line)

# Parse buyer info
for line in buyer_lines:
    key, value = extract_key_value_from_line(line)
    if key and value:
        result[f"Buyer {key}"] = value
    elif line:
        result.setdefault("Buyer Info", []).append(line)

# Extract key-value from 5th column (index 4)
table_rows = data[0]['tables'][0]
for row in table_rows:
    if len(row) > 4 and row[4]:
        cell = row[4]
        if '\n' in cell:
            parts = cell.split('\n', 1)
            key = parts[0].strip()
            value = parts[1].strip()
            result[key] = value
        else:
            result[cell.strip()] = ""

# Convert list-type values to string
for k in ["Company Info", "Buyer Info"]:
    if k in result:
        result[k] = "\n".join(result[k])

# ====================================
# Extract only actual item rows
# ====================================

item_rows = []
header_row = None

# Find the item table header row
for idx, row in enumerate(table_rows):
    if row and "Description of Goods" in row:
        header_row = row
        start_idx = idx + 1
        break

# Prepare header mapping
if header_row:
    headers = [h.replace('\n', ' ').strip() if h else "" for h in header_row]

    for row in table_rows[start_idx:]:
        if not any(row):  # skip completely empty rows
            continue

        # Skip rows that are NOT actual product line items
        if row[0] not in ["1", "2", "3"]:  # line items usually start with numeric index
            continue

        item = {}
        for i in range(len(headers)):
            if headers[i]:
                val = row[i] if i < len(row) and row[i] else ""
                key = headers[i]

                # Clean up Amount field
                if key == "Amount" and '\n' in val:
                    parts = val.split('\n')
                    item["Amount"] = parts[0].strip()
                    if len(parts) > 1:
                        item["Tax"] = parts[1].strip()
                    if len(parts) > 2:
                        item["Round Off"] = parts[2].strip()
                else:
                    item[key] = val.strip()

        # Fix key for "Sl No."
        if "Sl No." in item:
            item["Sl"] = item.pop("Sl No.")

        item_rows.append(item)
        break  # STOP after first real item only

# Add items if found
if item_rows:
    result["Items"] = item_rows

# Clean known encodings
result = json.loads(json.dumps(result).replace('(cid:299)', '').replace('\u2122', "'"))

# Print result
print(json.dumps(result, indent=4))
