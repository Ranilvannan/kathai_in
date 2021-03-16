from googletrans import Translator
from urllib.parse import urldefrag
import random
import string


def translate_text(text):
    result = ''
    try:
        translator = Translator()
        result = translator.translate(text)
    except:
        pass

    return result


def clean_url(url):
    """
    Clean URL
        1. Split the #
        2. Remove the ending /

    """

    new_url = ''
    if url:
        new_url = url.strip()
        new_url = urldefrag(new_url).url
        new_url = new_url.rstrip('/')

    return new_url


def generate_url(text):
    new_text = text.lower()
    new_text = new_text.replace(" ", "-")
    new_text = new_text.replace("'", "")
    new_text = new_text.replace(",", "")

    res = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
    site_path = "{0}-{1}".format(new_text, res)
    return site_path
