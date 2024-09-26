from transformers import MarianMTModel, MarianTokenizer

# Load the pre-trained translation model and tokenizer
model_name = 'Helsinki-NLP/opus-mt-en-de'  # Change to 'opus-mt-de-en' for German to English
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Example English text to translate
text = "Hello, how are you?"

# Prepare the text for translation (tokenization)
inputs = tokenizer(text, return_tensors="pt", padding=True)

# Generate the translation
translated_tokens = model.generate(**inputs)

# Decode the translation
translated_text = tokenizer.decode(translated_tokens[0], skip_special_tokens=True)
print(translated_text)
