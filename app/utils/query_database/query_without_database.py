import os
import json
import sys
sys.path.append('../')
from dotenv import load_dotenv
from utils.constants.constants import GROQ_CLIENT_LLAMAINDEX, FILES_OUTPUT_DIR
from llama_index.core.llms import ChatMessage

load_dotenv()

def chat_with_llm(user_info, user_prompt):
    """Chat with the LLM using the provided context JSON and user prompt."""
    llm = GROQ_CLIENT_LLAMAINDEX

    user_type = user_info['user_type']


    metadata_file_path = os.path.join(FILES_OUTPUT_DIR, "user_metadata.json")
    with open(metadata_file_path, 'r') as file:
        user_metadata = json.load(file)

    context_json = {}

    if user_type.lower() == "buyer":
        # Pass information for both sellers and landlords for rent
        sellers_info = next((entry for entry in user_metadata if entry["user_type"].lower() == "seller"), {})
        landlords_info = next((entry for entry in user_metadata if entry["user_type"].lower() == "landlord_for_rent"), {})
        context_json = {
            "sellers": sellers_info.get("information", []),
            "landlords_for_rent": landlords_info.get("information", [])
        }
    elif user_type.lower() == "seller":
        # Pass information for buyers
        context_json = next((entry for entry in user_metadata if entry["user_type"].lower() == "buyer"), {})
    elif user_type.lower() == "tenant":
        # Pass information for landlords
        context_json = next((entry for entry in user_metadata if entry["user_type"].lower() == "landlord_for_rent"), {})
    elif user_type.lower() == "landlord":
        # Pass information for tenants
        context_json = next((entry for entry in user_metadata if entry["user_type"].lower() == "tenant"), {})
    
    # If context_json is empty, return an error or handle accordingly
    if not context_json:
        return "No information available for the specified user type."
    
    # Convert user_info to a readable string format for LLM
    user_info_str = json.dumps(user_info, indent=4)

    # Prepare the system prompt message
    messages = [
        ChatMessage(
            role="system", content=(
                "You are a specialized real estate assistant. "
                "Your task is to answer questions about properties strictly based on the information provided in the JSON context. "
                "Respond directly and conversationally without explicitly mentioning the context. "
                "If a user is a buyer, you will only answer questions related to the properties available for sale and for rent, "
                "including details like name, property type, budget, and preferred location from the buyer's context. "
                "Do not provide information outside of this context."
                "The context is provided as follows: - If the user is a buyer, all seller's and landlord's context is provided. "
                "Here are the details of the user who is writing the query: \n"
                f"{user_info_str}\n"
                "And below is the information the user might be interested in: \n"
                f"{json.dumps(context_json, indent=4)}"
                "User will write query with the language he/she wants the output in for example user will write its query and at the end they will write LANGAUGE: German. so you must respond to user in that particular language."
            )
        ),
        ChatMessage(role="user", content=user_prompt),
    ]

    resp = llm.chat(messages)
    return resp.message.content