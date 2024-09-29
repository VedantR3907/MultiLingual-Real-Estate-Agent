import json
import sys
import os
from typing import List, Dict
import streamlit as st
from llama_index.core.llms import ChatMessage
sys.path.append('../../')
from utils.constants.constants import FILES_OUTPUT_DIR

DATABASE_FILE = os.path.join(FILES_OUTPUT_DIR, 'database.json')

async def read_chat_history(limit: int = 999999) -> List[Dict[str, str]]:
    try:
        with open(DATABASE_FILE, 'r') as file:
            data = json.load(file)
            # Return the last `limit` entries
            return data[-limit:]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def display_chat_history(chat_history: List[Dict[str, str]]):
    for entry in chat_history:
        if "user" in entry:
            with st.chat_message("HUMAN", avatar='./assets/user.png'):
                st.markdown(entry["user"])
        if "assistant" in entry:
            with st.chat_message("AI", avatar='./assets/meta.png'):
                st.markdown(entry["assistant"])


async def format_chat_history_llamaindex(chat_history: List[Dict[str, str]]) -> List[ChatMessage]:
    formatted_history = []
    
    for entry in chat_history:
        if "user" in entry:
            formatted_history.append(ChatMessage(
                role="user",
                content=entry["user"]
            ))
        if "assistant" in entry:
            formatted_history.append(ChatMessage(
                role="assistant",
                content=entry["assistant"]
            ))
    
    return formatted_history