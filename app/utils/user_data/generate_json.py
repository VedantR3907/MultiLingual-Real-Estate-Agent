import sys
import json
sys.path.append('../../')
from utils.constants.constants import FILES_OUTPUT_DIR

def load_user_metadata():
    """Load user metadata from the JSON file."""
    try:
        with open(f"{FILES_OUTPUT_DIR}/user_metadata.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return empty list if file does not exist or is invalid

def save_user_metadata(user_type, user_info):
    """Save user metadata to the JSON file."""
    metadata = load_user_metadata()
    
    # Find the right section for the user type
    user_type_key = user_type.lower()  # Convert to lowercase for consistency
    for entry in metadata:
        if entry["user_type"] == user_type_key:
            entry["information"].append(user_info)
            break
    else:
        # If the user type is not found, create a new entry
        metadata.append({
            "user_type": user_type_key,
            "information": [user_info]
        })
    
    # Write updated metadata back to the JSON file
    with open(f"{FILES_OUTPUT_DIR}/user_metadata.json", "w") as file:
        json.dump(metadata, file, indent=4)