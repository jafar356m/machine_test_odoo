from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'

    watermark_image = fields.Binary(string="Watermark Image")