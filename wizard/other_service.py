from odoo import models, fields, api


class OtherService(models.Model):
    _name = "other.service"
    _description = "Other Service"

    def trigger_validate_story(self):
        recs = self.env["story.book"].search([("is_valid", "=", False)])

        for rec in recs:
            self.mapping_parent(rec)
            valid = self.valid_story(rec)
            if valid:
                rec.is_valid = True

    def mapping_parent(self, obj):
        if obj.parent_url:
            if not obj.parent_id:
                story_obj = self.env["story.book"].search([("crawl_url", "=", obj.parent_url)])

                if story_obj:
                    obj.parent_id = story_obj.id

    def valid_story(self, obj):
        result = False
        status = False

        if obj.site_url \
                and obj.site_title \
                and obj.site_preview \
                and obj.tag_ids \
                and obj.crawl_domain \
                and obj.crawl_url \
                and obj.language \
                and obj.title \
                and obj.preview \
                and obj.content_ids:
            status = True

        if obj.parent_url and obj.parent_id and status:
            result = True
        elif (not obj.parent_url) and (not obj.parent_id) and status:
            result = True

        return result
