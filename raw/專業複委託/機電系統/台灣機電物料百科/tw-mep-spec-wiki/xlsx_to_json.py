import json
import os
import sys

try:
    import openpyxl
except ImportError:
    print("Error: The 'openpyxl' library is required to run this script.", file=sys.stderr)
    print("Please install it using: pip install openpyxl", file=sys.stderr)
    sys.exit(1)

def convert_xlsx_to_json(xlsx_path, json_path):
    try:
        # Load workbook with data_only=True to get values instead of formulas
        wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
        sheet = wb.active
        
        headers = []
        data = []
        
        for r_idx, row in enumerate(sheet.iter_rows(values_only=True)):
            if r_idx == 0:
                headers = list(row)
                continue
            
            # Skip completely empty rows
            if all(val is None for val in row):
                continue
                
            row_dict = {}
            for col_idx, val in enumerate(row):
                if col_idx < len(headers):
                    header_name = headers[col_idx]
                    if header_name:
                        # Convert "編號" to integer if possible
                        if header_name == "編號" and val is not None:
                            try:
                                val = int(float(val))  # float first to handle cases like 1.0
                            except (ValueError, TypeError):
                                pass
                        row_dict[header_name] = val
            data.append(row_dict)
            
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully converted {xlsx_path} to {json_path}")
    except Exception as e:
        print(f"Error during conversion: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    xlsx_path = os.path.normpath(os.path.join(script_dir, "..", "MEP品項百科.xlsx"))
    json_path = os.path.normpath(os.path.join(script_dir, "MEP品項百科.json"))
    
    convert_xlsx_to_json(xlsx_path, json_path)
