from odoo import models, fields, api, exceptions
from datetime import datetime


class ProjectSite1(models.Model):
    _name = "project.site1"
    _description = "Project Site 1"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    ref = fields.Char(string="Reference")
    date = fields.Date(string="Date", default=datetime.now())
    language = fields.Many2one(comodel_name="story.language", string="Language")

    site_url = fields.Text(string="URL")
    site_title = fields.Text(string="Title")
    site_preview = fields.Text(string="Preview")

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    content_ids = fields.One2many(comodel_name="story.content", inverse_name="story_id")

    category_id = fields.Many2one(comodel_name="story.tags", string="Category")
    prev_id = fields.Many2one(comodel_name="project.site1", string="Previous")
    date_of_publish = fields.Date(string="Date Of Publish")

    # Status
    is_valid = fields.Boolean(string="Valid", default=False)
    last_validate_on = fields.Date(string="Last Validate On")
    is_exported = fields.Boolean(string="Exported", default=False)
    has_published = fields.Boolean(string="Published", default=False)

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("project.site1")
        return super(ProjectSite1, self).create(vals)


class Site1Content(models.Model):
    _name = "site1.content"
    _description = "Site 1 Content"

    order_seq = fields.Integer(string="Order Sequence")
    content = fields.Text(string="Content")
    story_id = fields.Many2one(comodel_name="project.site1", string="Story")
