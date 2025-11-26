import subprocess
import os
import re

# --- Configuration ---
# File where successfully processed IDs are saved (ID \t FULL_PATH)
DATABASE_FILE = "extracted_ids.txt"
# Regex to extract the Model ID from the V-roid Hub URL structure:
# /models/(\d+) - captures the digits after /models/
URL_ID_PATTERN = re.compile(r'/models/(\d+)')

def load_existing_ids(db_file: str) -> set:
    """Loads all model IDs from the DATABASE_FILE into a set for quick lookup."""
    existing_ids = set()
    if not os.path.exists(db_file):
        print(f"Warning: Database file '{db_file}' not found. Starting with an empty set.")
        return existing_ids

    try:
        with open(db_file, "r", encoding='utf-8') as f:
            for line in f:
                # The format is ID \t FULL_PATH
                parts = line.strip().split('\t')
                if parts and parts[0].isdigit():
                    existing_ids.add(parts[0])
        print(f"Successfully loaded {len(existing_ids)} existing IDs from {db_file}.")
    except Exception as e:
        print(f"Error loading existing IDs from {db_file}: {e}")
    
    return existing_ids

def add_id_to_processed_list(model_id: str, link: str):
    """
    Appends the model ID and the source link (as a temporary 'path') to the DATABASE_FILE.
    This registers the ID as processed for future runs.
    """
    # Use the link as the 'path' since we don't have the final file path here.
    output_line = f"{model_id}\t[PROCESSED_FROM_LINK]:{link}\n"
    try:
        # 'a' mode appends to the file, creating it if it doesn't exist.
        with open(DATABASE_FILE, 'a', encoding='utf-8') as f:
            f.write(output_line)
        print(f"    [REGISTERED] ID {model_id} added to {DATABASE_FILE}.")
    except Exception as e:
        print(f"    [ERROR] Could not register ID {model_id} to {DATABASE_FILE}: {e}")


def extract_model_id_from_url(url: str) -> str | None:
    """Extracts the model ID (digits after /models/) from a given URL."""
    match = URL_ID_PATTERN.search(url)
    if match:
        return match.group(1) # Return the captured digits
    return None

# --- Main Program Logic ---

total = 0
fault = 0
ff = open("Needdownload.log","w")

# 1. Load the IDs that have already been processed
processed_ids = load_existing_ids(DATABASE_FILE)

try:
    with open("Needdownload.txt","r",encoding='utf-8') as f:
        for line in f:
            # Clean the line (remove leading/trailing whitespace and newlines)
            clean_line = line.strip() 

            if not clean_line or clean_line.startswith('#'):
                # Skip blank lines or lines starting with a comment hash
                continue
            
            # 2. Extract the model ID from the URL
            model_id = extract_model_id_from_url(clean_line)

            if not model_id:
                print(f"Skipping link (No Model ID found): {clean_line}")
                continue

            # 3. Check if the model ID is already processed
            if model_id in processed_ids:
                print(f"--- SKIPPING --- ID {model_id} already exists in {DATABASE_FILE}.")
                continue
            
            # --- If ID is new, proceed with execution ---
            total += 1
            command = 'node '+ ' src/index.js ' + clean_line
            print(str(total) + "-Running: " + command)
            
            # Execute the external command
            result = subprocess.run(command, capture_output = True, shell = True)
            
            # 4. Success/Failure Check and Registration
            
            is_success = (result.stderr == None or result.stderr == b'')
            
            # Logging
            ff.write("---------------------NEW LINK-------------------\n")
            ff.write(clean_line + '\n')
            ff.write(f"MODEL ID: {model_id}\n")
            
            ff.write("------STDOUT-------\n")
            if (result.stdout == None):
                print(f'STDout ERROR {clean_line}')
                ff.write("NO OUTPUT!\n")
            else:
                ff.write(str(result.stdout) + '\n')
            
            ff.write("------STDERR-------\n")
            if is_success:
                print(f'OK! {clean_line}')
                ff.write("No error!\n")
                
                # IMPORTANT: Register the ID after successful processing!
                add_id_to_processed_list(model_id, clean_line)
                processed_ids.add(model_id) # Add to the set for runtime skipping
                
            else:
                ff.write(str(result.stderr) + '\n')
                print("-----ERROR!! READ LOGS-----")
                fault += 1
            
            ff.write("---------------------END LINK-------------------\n\n\n")

finally:
    ff.close()
    print("\n==================================")
    print("DONE!")
    print(f"Total links processed this run: {total}")
    print(f"Faults: {fault}")
    print("==================================")
#input("Press anykey to exit")
