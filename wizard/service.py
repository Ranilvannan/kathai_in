from odoo import models, fields, api


class Service(models.Model):
    _name = "service.service"
    _description = "Service"

    def desitales2_crawl(self):
        self.env["crawl.service"].trigger_desitales2_crawl()

    def reset_all(self):
        self.env["other.service"].trigger_reset()

    def refresh_validation_all(self):
        self.env["other.service"].trigger_refresh_validation()

    def validate_story_all(self):
        self.env["other.service"].trigger_validate_story()

    def publish_all(self):
        self.env["publish.service"].trigger_publish()

    def export_all(self):
        self.env["story.export"].trigger_export()

