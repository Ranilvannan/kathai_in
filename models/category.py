from odoo import models, fields


class StoryCategory(models.Model):
    _name = "story.category"
    _description = "Story Category"
    _rec_name = "name"

    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
    description = fields.Text(string="Description")
    tag_ids = fields.One2many(comodel_name="category.tag", inverse_name="category_id")


class CategoryTag(models.Model):
    _name = "category.tag"
    _description = "Category Tag"
    _rec_name = "name"

    name = fields.Char(string="Name")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")

    def trigger_generate_tag(self):
        recs = self.env["story.book"].search([("is_cat_checked", "=", False)])[:100]

        for rec in recs:
            tag = self.env["category.tag"].search([("name", "=", rec.category)])
            if not tag:
                self.env["category.tag"].create({"name": rec.category})

            rec.write({"is_cat_checked": True})
