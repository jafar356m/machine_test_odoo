from odoo import models, fields, api

class SampleMaterial(models.Model):
    _name = 'sample.material'
    _description = 'Sample Material Requirement'

    sample_id = fields.Many2one('sample.submission', string="Sample Submission", ondelete='cascade', required=True)
    sl_no = fields.Integer(string="Sl No")
    material_id = fields.Many2one('product.product', string="Material", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    remarks = fields.Text(string="Remarks")
