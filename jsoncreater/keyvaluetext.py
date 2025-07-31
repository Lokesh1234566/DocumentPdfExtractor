import json

# ------------------------------
# Load JSON File
# ------------------------------
with open('../pdf/B1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

result = {}

# ------------------------------
# Extract Company and Buyer Info
# ------------------------------
header_block = data[0]['tables'][0][0][0]
lines = header_block.split('\n')

def extract_key_value_from_line(line):
    if ':' in line:
        key, value = line.split(':', 1)
        return key.strip(), value.strip()
    elif ' : ' in line:
        key, value = line.split(' : ', 1)
        return key.strip(), value.strip()
    return None, None

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

for line in company_lines:
    key, value = extract_key_value_from_line(line)
    if key and value:
        result[key] = value
    elif line:
        result.setdefault("Company Info", []).append(line)

for line in buyer_lines:
    key, value = extract_key_value_from_line(line)
    if key and value:
        result[f"Buyer {key}"] = value
    elif line:
        result.setdefault("Buyer Info", []).append(line)

for k in ["Company Info", "Buyer Info"]:
    if k in result:
        result[k] = "\n".join(result[k])

# ------------------------------
# Extract Key-Value Pairs in Column 5
# ------------------------------
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

# ------------------------------
# Extract and Merge Item Rows
# ------------------------------
item_rows = []
header_row = None
start_idx = None

# Find header row
for idx, row in enumerate(table_rows):
    if row and any("Description of Goods" in str(cell) for cell in row):
        header_row = row
        start_idx = idx + 1
        break

if header_row and start_idx is not None:
    headers = [cell.replace("\n", " ").strip() if cell else "" for cell in header_row]
    data_row = table_rows[start_idx]
    split_columns = [cell.split("\n") if cell else [] for cell in data_row]
    max_len = max(len(col) for col in split_columns)

    for i in range(0, max_len - 1, 2):  # Step every 2 lines
        for j in range(2):  # Handle 2 entries per pair
            item = {}
            for col_idx, col_values in enumerate(split_columns):
                key = headers[col_idx]
                if not key:
                    continue

                val1 = col_values[i + j] if i + j < len(col_values) else ""
                val2 = col_values[i + j + 1] if (key == "Description of Goods" and i + j + 1 < len(col_values)) else ""

                if key == "Description of Goods":
                    item[key] = f"{val1.strip()} {val2.strip()}".strip()
                elif key == "Sl No.":
                    item["Sl"] = val1.strip()
                else:
                    item[key] = val1.strip()
            if item.get("Sl") and item.get("Description of Goods"):
                item_rows.append(item)

# Add to result
if item_rows:
    result["Items"] = item_rows

# ------------------------------
# Clean and Output Result
# ------------------------------
result = json.loads(json.dumps(result).replace('(cid:299)', '').replace('\u2122', "'"))

# Print JSON
print(json.dumps(result, indent=4))

# Optional: Save to file
# with open("output.json", "w", encoding="utf-8") as out_file:
#     json.dump(result, out_file, indent=4, ensure_ascii=False)
