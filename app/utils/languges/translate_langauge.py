from transformers import MarianMTModel, MarianTokenizer

# Load the pre-trained translation model and tokenizer

def translate_language(language: str, text: str):
    model_name = f'Helsinki-NLP/opus-mt-{language}-en'  # Change to 'opus-mt-de-en' for German to English
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)

    # Prepare the text for translation (tokenization)
    inputs = tokenizer(text, return_tensors="pt", padding=True)

    # Generate the translation
    translated_tokens = model.generate(**inputs)

    # Decode the translation
    translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
    
    return translated_text