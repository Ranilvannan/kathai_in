from odoo import models, fields, api, exceptions
from datetime import datetime
from googletrans import Translator

CRAWL_STATUS = [("url_crawl", "URL Crawl"), ("content_crawl", "Content Crawl")]
STATUS = [("draft", "Draft"), ("publish", "Publish")]


class StoryBook(models.Model):
    _name = "story.book"
    _description = "Story Book"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    date = fields.Date(string="Date", default=datetime.now())

    # CRAWL INFO
    crawl_domain = fields.Char(string="Domain")
    crawl_url = fields.Text(string="URL")
    parent_url = fields.Text(string="Parent URL")
    crawl_status = fields.Selection(selection=CRAWL_STATUS, string="Crawl Status")
    language = fields.Many2one(comodel_name="story.language")

    # SITE INFO
    site_url = fields.Text(string="URL")
    site_title = fields.Text(string="Title")
    site_preview = fields.Text(string="Preview")
    tag_ids = fields.Many2many(comodel_name="story.tags")
    parent_id = fields.Many2one(comodel_name="story.book")
    has_published = fields.Boolean(string="Has Published", default=False)
    is_exported = fields.Boolean(string="Is Exported", default=False)
    date_of_publish = fields.Date(string="Date Of Publish")

    # CONTENT
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    def trigger_english_title(self):
        translator = Translator()
        title = translator.translate(self.title)

        result = title.text
        self.site_title = title.text

        new_result = result.lower()
        new_result = new_result.replace(" ", "-")
        new_result = new_result.replace("'", "")
        new_result = new_result.replace(",", "")
        self.site_url = new_result

        preview = translator.translate(self.preview)
        self.site_preview = preview.text

    def trigger_publish(self):
        if self.crawl_status != "content_crawl":
            raise exceptions.ValidationError("Error! Story must be publish after CONTENT CRAWL")

        if self.parent_url and (not self.parent_id):
            obj = self.env["story.book"].search([("crawl_url", "=", self.parent_url)])
            if obj:
                self.parent_id = obj.id
            else:
                raise exceptions.ValidationError("Error! Parent not found")

        parent_id_setup = True
        rec = self
        while parent_id_setup:
            if rec.parent_id and rec.parent_url:
                if not rec.parent_id.has_published:
                    rec.parent_id.has_published = True
                rec = rec.parent_id
            else:
                parent_id_setup = False

        self.date_of_publish = datetime.now()
        self.has_published = True

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("story.book")
        return super(StoryBook, self).create(vals)


class StoryContent(models.Model):
    _name = "story.content"
    _description = "Story Content"

    order_seq = fields.Integer(string="Order Sequence")
    content = fields.Text(string="Content")
    story_id = fields.Many2one(comodel_name="story.book", string="Story")

