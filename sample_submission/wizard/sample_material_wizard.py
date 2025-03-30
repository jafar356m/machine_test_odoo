from odoo import models, fields, api

class SampleMaterialWizard(models.TransientModel):
    _name = 'sample.material.wizard'
    _description = 'Sample Material Wizard'

    sample_id = fields.Many2one('sample.submission', string="Sample Submission", required=True)
    sl_no = fields.Integer(string="Sl No")
    material_id = fields.Many2one('product.product', string="Material", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    remarks = fields.Text(string="Remarks")

    def apply_material(self):
        """Save the material details to the sample.material model linked to sample.submission."""
        self.env['sample.material'].create({
            'sample_id': self.sample_id.id,
            'sl_no': self.sl_no,
            'material_id': self.material_id.id,
            'quantity': self.quantity,
            'remarks': self.remarks,
        })







