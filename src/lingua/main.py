from pymystem3 import Mystem

async def lemmatize(text):
    m = Mystem()
    lemmatized_text = m.lemmatize(text)

    cleaned_list = [string for string in lemmatized_text if not string.isspace(
    ) and not string.isnumeric()]

    return (cleaned_list)

import unicodedata

def normalize(text):
    return unicodedata.normalize('NFKC', text).casefold()


import re

async def concordance(text: str, target_word: str) -> str:
    def normalize(s: str) -> str:
        # Ваша нормализация, которая должна быть определена
        return s.lower()

    normalized_text = normalize(text)
    normalized_target_word = normalize(target_word)

    text_arr = normalized_text.split()
    indices = [i for i, word in enumerate(text_arr) if normalized_target_word in normalize(word)]

    if not indices:
        return "Target word not found in the text."

    # For simplicity, taking the first occurrence
    index = indices[0]

    # Prepare the concordance string
    if index == 0:
        concordance_str = f"{text_arr[index]} {text_arr[index + 1]} {text_arr[index + 2]}..."
    elif index == len(text_arr) - 1:
        concordance_str = f"...{text_arr[index - 2]} {text_arr[index - 1]} {text_arr[index]}"
    else:
        concordance_str = f"...{text_arr[index - 2]} {text_arr[index - 1]} {text_arr[index]} {text_arr[index + 1]} {text_arr[index + 2]}..."

    # Highlight the target words with Tailwind CSS classes
    highlighted_concordance = re.sub(f"({re.escape(target_word)})", r'<mark class="bg-yellow-300">\1</mark>', concordance_str, flags=re.IGNORECASE)

    return highlighted_concordance

