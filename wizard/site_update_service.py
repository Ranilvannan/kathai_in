from odoo import models, fields
import string
import random
from itertools import groupby
from operator import itemgetter
import unicodedata


class SiteUpdateService(models.TransientModel):
    _name = "site.update.service"
    _description = "Site Update Service"

    def get_url(self, text):
        result = self.translate(text)
        striped_text = self.strip_accents(result)
        return self.generate_url(striped_text)

    def strip_accents(self, text):
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)

    def generate_url(self, text):
        new_text = "".join([c if c.isalnum() else "_" for c in text.lower()])
        new_text = "".join(map(next, map(itemgetter(1), groupby(new_text))))
        res = "".join(random.choices(string.ascii_lowercase + string.digits, k=7))
        site_path = "{0}_{1}".format(new_text, res)
        return site_path

    def translate(self, text):
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
