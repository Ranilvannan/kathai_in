from bs4 import BeautifulSoup
from googletrans import Translator
from urllib.parse import urldefrag
import requests
import random
import string


def translate_text(text):
    result = ''
    try:
        translator = Translator()
        result = translator.translate(text)
        result = result.text
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


def get_url_content(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup
