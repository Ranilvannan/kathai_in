from odoo import models, fields, api
from datetime import datetime


class ProjectSite3(models.Model):
    _name = "project.site3"
    _description = "Project Site 3 hindisexstory.osholikes"
    _rec_name = "name"
    _language = "Hindi"
    _blog_code = "Hindi"

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
    prev_id = fields.Many2one(comodel_name="project.site3", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site3", string="Next")
    is_valid = fields.Boolean(string="Valid", default=False)
    last_checked_on = fields.Date(string="Last Checked On")
    is_exported = fields.Boolean(string="Exported", default=False)
    published_on = fields.Date(string="Published On")

    @api.model
    def create(self, vals):
        vals["name"] = self.env['ir.sequence'].next_by_code("project.site3")
        vals["url"] = self.env["site.update.service"].get_url(vals["title"])
        return super(ProjectSite3, self).create(vals)
