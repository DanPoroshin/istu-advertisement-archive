from pymystem3 import Mystem


async def lemmatize(text):
    m = Mystem()
    lemmatized_text = m.lemmatize(text)

    cleaned_list = [string for string in lemmatized_text if not string.isspace(
    ) and not string.isnumeric()]

    return (cleaned_list)
