import string


def extract_words(text: str) -> list[str]:
    accepted_chars = ['‘', '-', ' ']
    accepted_chars.extend(string.ascii_lowercase)

    new_string = ""

    for char in text:
        if char.lower() in accepted_chars:
            new_string += char

    return new_string.split(' ')
