import sys
import asyncio
import google.generativeai as genai
sys.path.append('../')
from utils.constants.constants import GEMINI_API_KEY, GEMINI_MODEL
from utils.chat_history.image_chat_history import write_image_chat_to_json, read_chat_history_image

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(GEMINI_MODEL)

messages = read_chat_history_image(limit=2)

def chat_image(image_path: str, query: str):
    myfile = genai.upload_file(image_path)

    result = model.generate_content(
        [myfile, "\n\n",f"The user query is {query} and the chat history between user and model is {messages} in the language user wants, user will write the langauge they want response in and you must respond in that particular langauge."]
    )


    write_image_chat_to_json(query, 'user')
    write_image_chat_to_json(result.text, 'model')

    return result.text


# asyncio.run(generate_image_description('E:/Codes/Data Sciene/AI/Real_Estate_Chatbot/app/assets/francesca-tosolini-tHkJAMcO3QE-unsplash.jpg', 'Whats in the image'))