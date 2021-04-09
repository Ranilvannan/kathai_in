from odoo import models, fields


class StoryCategory(models.Model):
    _name = "story.category"
    _description = "Story Category"
    _rec_name = "name"

    language = fields.Many2one(comodel_name="story.language")
    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
    description = fields.Text(string="Description")


class CategoryTag(models.Model):
    _name = "category.tag"
    _description = "Category Tag"
    _rec_name = "name"

    name = fields.Char(string="Name")
    language = fields.Many2one(comodel_name="story.language")
    category_id = fields.Many2one(comodel_name="story.category", string="Category")

    _sql_constraints = [
        ('name_uniq', 'unique (name, language)', 'Tag must be unique')
    ]

    def trigger_generate_tag(self):
        recs = self.env["story.book"].search([("is_cat_checked", "=", False)])[:100]

        for rec in recs:
            tag = self.env["category.tag"].search([("name", "=", rec.category), ("language", "=", rec.language.id)])
            if not tag:
                self.env["category.tag"].create({"name": rec.category, "language": rec.language.id})

            rec.write({"is_cat_checked": True})
