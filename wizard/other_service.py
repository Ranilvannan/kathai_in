from odoo import models, fields, api
from datetime import datetime


class OtherService(models.Model):
    _name = "other.service"
    _description = "Other Service"

    def trigger_refresh_validation(self):
        recs = self.env["story.book"].search([("is_valid", "=", False),
                                              ("last_validate_on", "!=", datetime.now())])[:100]

        for rec in recs:
            rec.write({"last_validate_on": False})

    def trigger_validate_story(self):
        recs = self.env["story.book"].search([("is_valid", "=", False),
                                              ("last_validate_on", "=", False)])[:10]

        for rec in recs:
            self.mapping_parent(rec)
            valid = self.check_valid_story(rec)
            rec.write({"is_valid": True if valid else False,
                       "last_validate_on": datetime.now()})

    def mapping_parent(self, obj):
        if obj.parent_url:
            if not obj.parent_id:
                story_obj = self.env["story.book"].search([("crawl_url", "=", obj.parent_url)])

                if story_obj:
                    obj.parent_id = story_obj.id

    def check_valid_story(self, obj):
        result = False

        if obj.site_url \
                and obj.site_title \
                and obj.site_preview \
                and obj.crawl_domain \
                and obj.crawl_url \
                and obj.language \
                and obj.title \
                and obj.preview \
                and obj.content_ids:
            result = True

        if obj.parent_url:
            if not obj.parent_id:
                result = False

        if obj.parent_id:
            if not obj.parent_id.is_exported:
                result = False

        for tag in obj.tag_ids:
            if (not tag.name) or (not tag.url):
                result = False

        return result

    def trigger_reset(self):
        recs = self.env["story.book"].search([])

        for rec in recs:
            rec.write({"is_valid": False,
                       "last_validate_on": False,
                       "is_exported": False,
                       "date_of_publish": False,
                       "has_published": False})
