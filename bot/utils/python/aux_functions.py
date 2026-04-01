import os
import json
import re

def clean_and_load_json(raw_string):
    clean_str = re.sub(r"```json|```", "", raw_string).strip()
    clean_str = re.sub(r",\s*([\]}])", r"\1", clean_str)
    
    try:
        return json.loads(clean_str)
    except json.JSONDecodeError as e:
        print(f"❌ Still failing at: {e}")
        start = clean_str.find('[')
        end = clean_str.rfind(']') + 1
        return json.loads(clean_str[start:end])
    
    
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)