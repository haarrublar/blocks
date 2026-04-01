import json

# Configuration
json_file_path = "./components_table.json"
target_session = "bf819f56-a996-4769-9f39-63a62482a5ff"
output_file = "pavilion_commands.txt"

def extract_session_commands(file_path, session_id, output_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Access the specific session
        session_data = data.get(session_id)
        
        if not session_data:
            print(f"Error: Session {session_id} not found in the JSON.")
            return

        cleaned_commands = []

        # Iterate through the part groups (e.g., "1", "2") inside the session
        for part_group in session_data.values():
            for component in part_group:
                commands = component.get("Commands", [])
                
                for cmd in commands:
                    # Clean: remove quotes, slashes, and trailing commas
                    clean_cmd = cmd.replace('"', '').replace('/', '').replace(',', '').strip()
                    
                    if clean_cmd:
                        cleaned_commands.append(clean_cmd)

        # Save to file
        with open(output_path, "w") as f:
            for command in cleaned_commands:
                f.write(f"{command}\n")
                
        print(f"Success! {len(cleaned_commands)} commands written to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Run the extraction
extract_session_commands(json_file_path, target_session, output_file)