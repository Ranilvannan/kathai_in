from odoo import models, fields
from odoo.tools import config
from datetime import datetime
import os
import base64


class Gallery(models.Model):
    _name = "blog.gallery"
    _description = "Blog Galleries"
    _rec_name = "filename"

    date = fields.Date(string="Date", default=datetime.now())
    filename = fields.Char(string="Filename")
    filepath = fields.Char(string="Filepath")
    image = fields.Binary(string="Image")
    description = fields.Char(string="Description")
    is_exported = fields.Boolean(string="Is Exported")

    def trigger_gallery(self):
        root_path = config["gallery_path"]
        filepath = os.path.join(root_path, self.filepath)
        image = os.path.join(filepath, self.filename)
        is_directory_available = os.path.isdir(filepath)

        if not is_directory_available:
            os.makedirs(filepath)

        data = base64.b64decode(self.image)
        with open(image, "wb") as imgFile:
            imgFile.write(data)

        self.image = False
