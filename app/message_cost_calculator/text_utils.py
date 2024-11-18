import string


def remove_non_supported_characters(text: str):
    accepted_chars = ['‘', '-',' ']
    accepted_chars.extend(string.ascii_lowercase)

    new_string = ""

    for char in text.lower():
        if char in accepted_chars:
            new_string += char

    return new_string
