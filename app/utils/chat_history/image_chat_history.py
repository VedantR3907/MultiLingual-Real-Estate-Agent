import json
import os
import sys
from typing import List, Dict
sys.path.append('../../')
from utils.constants.constants import FILES_OUTPUT_DIR

file_path = os.path.join(FILES_OUTPUT_DIR, 'image_database.json')

def write_image_chat_to_json(text: str, user_type: str):
    # Prepare the data to be stored in JSON format
    data = {
        "role": user_type,
        "parts": text
    }

    # Initialize an empty list for existing data
    existing_data = []

    # Check if the JSON file already exists
    if os.path.exists(file_path):
        # If the file exists, read the existing data
        with open(file_path, 'r') as f:
            try:
                existing_data = json.load(f)  # Load existing data from the file
            except json.JSONDecodeError:
                existing_data = []  # In case of empty file or corrupted JSON

    # Append the new data to the existing data
    existing_data.append(data)

    # Save the updated data back to the JSON file
    with open(file_path, 'w') as f:
        json.dump(existing_data, f, indent=4)



def read_chat_history_image(limit: int = 999999) -> List[Dict[str, str]]:
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            # Return the last `limit` entries
            return data[-limit:]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_uploaded_image(uploaded_file):
    # Create the 'app/assets' directory if it doesn't exist
    p = os.path.dirname(__file__).split('\\')[:-2]
    joined_path = '\\'.join(p)

    save_dir = os.path.join(joined_path, 'assets')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Save the uploaded image
    image_path = os.path.join(save_dir, uploaded_file.name)
    with open(image_path, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Write the contents of the uploaded file
    return image_path  # Return the path for further use
