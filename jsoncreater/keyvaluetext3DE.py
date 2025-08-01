import json
import ThreeDConstants
import os
# ------------------------------
# Load JSON File
# ------------------------------
input_path = '../pdf/G.json'
with open(input_path, 'r', encoding='utf-8') as f:
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
    if line.strip() == ThreeDConstants.Constant_3DEBuyer:
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
        result.setdefault(ThreeDConstants.Constant_Company_Info, []).append(line)

for line in buyer_lines:
    key, value = extract_key_value_from_line(line)
    if key and value:
        result[f"Buyer {key}"] = value
    elif line:
        result.setdefault(ThreeDConstants.Constant_Buyer_Info, []).append(line)

for k in [ThreeDConstants.Constant_Company_Info, ThreeDConstants.Constant_Buyer_Info]:
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
    if row and any(ThreeDConstants.Constant_Description in str(cell) for cell in row):
        header_row = row
        start_idx = idx + 1
        break

if header_row and start_idx is not None:
    headers = [cell.replace("\n", " ").strip() if cell else "" for cell in header_row]
    data_row = table_rows[start_idx]
    split_columns = [cell.split("\n") if cell else [] for cell in data_row]
    max_len = max(len(col) for col in split_columns)

    for i in range(0, max_len - 1, 2):
        for j in range(2):
            item = {}
            for col_idx, col_values in enumerate(split_columns):
                key = headers[col_idx]
                if not key:
                    continue

                val1 = col_values[i + j] if i + j < len(col_values) else ""
                val2 = col_values[i + j + 1] if (key == ThreeDConstants.Constant_Description and i + j + 1 < len(col_values)) else ""

                if key == ThreeDConstants.Constant_Description:
                    item[key] = f"{val1.strip()} {val2.strip()}".strip()
                elif key == ThreeDConstants.Constant_SL_No:
                    item[ThreeDConstants.Constant_Sl] = val1.strip()
                else:
                    item[key] = val1.strip()

            if item.get(ThreeDConstants.Constant_Sl) and item.get(ThreeDConstants.Constant_Description):
                item_rows.append(item)

if item_rows:
    result[ThreeDConstants.Constant_Items] = item_rows

# ------------------------------
# Extract Footer Info
# ------------------------------
footer_text_block = None
amount_chargeable_line = None
hsn_summary_rows = []
hsn_headers = []
declaration_lines = []
auth_signatory = ""

last_page_tables = data[-1]['tables']
for table in last_page_tables:
    for row in table:
        for cell in row:
            if not cell:
                continue
            if isinstance(cell, str):
                if ThreeDConstants.Constant_Amount_Charageable in cell:
                    amount_chargeable_line = cell
                elif ThreeDConstants.Constant_Tax_Amount_words in cell:
                    footer_text_block = cell
                elif ThreeDConstants.Constant_Declaration in cell:
                    declaration_lines.append(cell)
                elif ThreeDConstants.constant_Authorised_Signatory in cell and "for" in cell:
                    auth_signatory = cell
        if any(ThreeDConstants.Constant_HSN_SAC in (cell or "") for cell in row):
            hsn_headers = [c.strip().replace('\n', ' ') if c else "" for c in row]
            continue
        elif hsn_headers and any(cell for cell in row):
            hsn_summary_rows.append([c.strip().replace('\n', ' ') if c else "" for c in row])

# Extract: Amount Chargeable (in words)
if amount_chargeable_line:
    parts = amount_chargeable_line.split(ThreeDConstants.Constant_Amount_Charageable)
    if len(parts) > 1:
        result[ThreeDConstants.Constant_Amount_Charageable] = parts[1].replace("E. & O.E", "").strip()

# Extract: Tax Amount (in words) and Bank details
if footer_text_block:
    lines = footer_text_block.split("\n")
    for line in lines:
        if ThreeDConstants.Constant_Tax_Amount_words in line:
            result[ThreeDConstants.Constant_Tax_Amount_words] = line.split(":", 1)[-1].strip()
        elif ThreeDConstants.Constant_BankName in line or ThreeDConstants.COnstant_Account_no in line or ThreeDConstants.Constant_Branch_IFS in line:
            key, value = extract_key_value_from_line(line)
            if key and value:
                result[f"Bank {key}"] = value

# Extract: only one valid HSN Summary to root level
if hsn_headers and hsn_summary_rows:
    for row in hsn_summary_rows:
        row_dict = {}
        for i, cell in enumerate(row):
            if i < len(hsn_headers):
                key = hsn_headers[i].strip()
                value = cell.strip()
                if key and value:
                    row_dict[key] = value

        hsn_sac = row_dict.get(ThreeDConstants.Constant_HSN_SAC, "")
        if hsn_sac == "39269099":
            result[ThreeDConstants.Constant_HSN_SAC] = hsn_sac
            result[ThreeDConstants.Constant_Tax_value] = row_dict.get(ThreeDConstants.Constant_Tax_value, "")
            result[ThreeDConstants.Constant_integrated_tax] = row_dict.get(ThreeDConstants.Constant_integrated_tax, "")
            result[ThreeDConstants.Constant_Total_tax_amt] = row_dict.get(ThreeDConstants.Constant_Total_tax_amt, "")
            break

# Extract: Declaration
for block in declaration_lines:
    lines = block.split("\n")
    declaration_text = []
    for line in lines:
        if ThreeDConstants.Constant_Declaration in line or ThreeDConstants.constant_Authorised_Signatory in line:
            continue
        declaration_text.append(line.strip())
    if declaration_text:
        result[ThreeDConstants.Constant_Declaration] = " ".join(declaration_text).strip()

# Extract: Authorised Signatory
if auth_signatory:
    lines = auth_signatory.split("\n")
    result[ThreeDConstants.constant_Authorised_Signatory] = lines[-1].strip() if lines else auth_signatory.strip()

# ------------------------------
# Clean and Output Result
# ------------------------------
result = json.loads(json.dumps(result).replace(ThreeDConstants.Constant_cid299, '').replace(ThreeDConstants.Constant_u2122, "'"))

# Print JSON
print(json.dumps(result, indent=4, ensure_ascii=False))

# Save to keyvaluejson folder
# ------------------------------
input_filename = os.path.basename(input_path)
output_filename = os.path.splitext(input_filename)[0] + '.json'
output_folder = 'keyvaluejson'

os.makedirs(output_folder, exist_ok=True)

with open(os.path.join(output_folder, output_filename), 'w', encoding='utf-8') as out_file:
    json.dump(result, out_file, indent=4, ensure_ascii=False)
