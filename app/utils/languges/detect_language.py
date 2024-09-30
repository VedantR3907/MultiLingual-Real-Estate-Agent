from langdetect import detect


def detect_language(text: str):
    language = detect(text)
    
    return language
