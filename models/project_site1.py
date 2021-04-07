from odoo import models, fields, api
from odoo.tools import config
import os
from datetime import datetime
import random

LANGUAGE = "English"


class ProjectSite1(models.Model):
    _name = "project.site1"
    _description = "Project Site 1 sexstory.osholikes"
    _rec_name = "name"

    name = fields.Char(string="Name", readonly=True)
    ref = fields.Char(string="Reference")
    date = fields.Date(string="Date", default=datetime.now())

    site_url = fields.Text(string="Site URL")
    site_title = fields.Text(string="Site Title")
    site_preview = fields.Text(string="Site Preview")

    title = fields.Text(string="Title")
    preview = fields.Text(string="Preview")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")
    content_ids = fields.One2many(comodel_name="site1.content", inverse_name="story_id")

    prev_id = fields.Many2one(comodel_name="project.site1", string="Previous")
    next_id = fields.Many2one(comodel_name="project.site1", string="Next")

    # Status
    is_valid = fields.Boolean(string="Valid", default=False)
    last_checked_on = fields.Date(string="Last Checked On")
    is_exported = fields.Boolean(string="Exported", default=False)

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
