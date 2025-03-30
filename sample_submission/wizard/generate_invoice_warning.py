from odoo import models, fields, api, _
from odoo.exceptions import UserError


class GenerateInvoiceWarning(models.TransientModel):
    _name = 'generate.invoice.warning'
    _description = 'Invoice Generation Warning'

    sample_submission_id = fields.Many2one('sample.submission', string='Sample Submission')
    price = fields.Float(string='Price')
    discount = fields.Float(string='Discount')

    def action_confirm(self):
        self.ensure_one()
        submission = self.sample_submission_id

        # Create invoice
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': submission.customer_id.id,
            'invoice_date': fields.Date.today(),
            'invoice_origin': submission.name,
            'invoice_line_ids': [(0, 0, {
                'name': submission.name,
                'quantity': 1,
                'price_unit': self.price,
                'discount': self.discount,
                'tax_ids': [(6, 0, self.env['account.tax'].search([('type_tax_use', '=', 'sale')]).ids)],
            })]
        }
        invoice = self.env['account.move'].create(invoice_vals)

        # Update sample submission with invoice info
        submission.write({
            'invoice_id': invoice.id,
            'invoice_generated': True
        })
        submission.stage = 'completed'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }
