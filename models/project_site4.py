from odoo import models, fields, api
from datetime import datetime


class ProjectSite4(models.Model):
    _name = "project.site4"
    _description = "Project Site 4 malayalamsexstory.osholikes"
    _rec_name = "name"
    _language = "Malayalam"
    _blog_code = "Malayalam"

    name = fields.Char(string="Name", readonly=True)
    ref = fields.Char(string="Reference")
    date = fields.Date(string="Date", default=datetime.now())
    url = fields.Text(string="URL")
    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")
    content = fields.Text(string="Content")
    language = fields.Many2one(comodel_name="story.language", string="Language")
    gallery_id = fields.Many2one(comodel_name="blog.gallery", string="Gallery")
    gallery_ids = fields.Many2many(comodel_name="blog.gallery", string="Galleries")
    prev_id = fields.Many2one(comodel_name="project.site4", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site4", string="Next")
    is_valid = fields.Boolean(string="Valid", default=False)
    last_checked_on = fields.Date(string="Last Checked On")
    is_exported = fields.Boolean(string="Exported", default=False)
    published_on = fields.Date(string="Published On")

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("project.site4")
        return super(ProjectSite4, self).create(vals)
