from odoo import models, fields


class StoryCategory(models.Model):
    _name = "story.category"
    _description = "Story Category"
    _rec_name = "name"

    name = fields.Char(string="Name")
    url = fields.Char(string="URL")


class CategoryTag(models.Model):
    _name = "category.tag"
    _description = "Category Tag"
    _rec_name = "name"

    name = fields.Char(string="Name")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tag must be unique')
    ]

    def trigger_generate_tag(self):
        tags = self.env["category.tag"].search([])
        tag_list = [tag.name for tag in tags]

        rec = self.env["story.book"].search([("category", "not in", tag_list)])[1]
        self.env["category.tag"].create({"name": rec.category})
