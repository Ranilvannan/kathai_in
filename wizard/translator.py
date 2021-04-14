import unicodedata


def translate(text):
    result = ""

    if text:
        text = text.lower()
        english = []

        last_character = ""
        for letter in text:
            try:
                name = unicodedata.name(letter)
                character = name.split()
                current_character = character[-1]
            except:
                name = " "

            if "LETTER" in name:
                english.append(last_character)
                last_character = current_character
            elif "VOWEL SIGN" in name:
                last_character = "{0}{1}".format(last_character[:-1], current_character)
            elif "SIGN" in name:
                last_character = last_character[:-1]
            else:
                english.append(last_character)
                last_character = letter

        english.append(last_character)
        result = "".join(english)
        result = result.lower()
    return result

