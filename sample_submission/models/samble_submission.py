from importlib.resources import _
from odoo import models, fields, api
from odoo.exceptions import UserError

INVOICE_STATUS = [
    ('upselling', 'Upselling Opportunity'),
    ('invoiced', 'Fully Invoiced'),
    ('to invoice', 'To Invoice'),
    ('no', 'Nothing to Invoice')
]

class SampleSubmission(models.Model):
    _name = 'sample.submission'
    _description = 'Sample Submission'
    _rec_name = 'sequence'
    _order = 'sequence desc'

    sequence = fields.Char(string="Sequence Number", required=True, copy=False, readonly=True,
                           default=lambda self: _('New'))
    name = fields.Char(string="Name of Sample", required=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    submission_date = fields.Date(string="Date of Submission", default=fields.Date.context_today, required=True)
    description = fields.Text(string="Description")
    price = fields.Float(string="Price")
    discount = fields.Float(string="Discount (%)")
    vat = fields.Float(string="VAT (%)", default=0.0)
    total_price = fields.Float(string="Amount", compute='_compute_total_price', store=True)
    stage = fields.Selection([
        ('pending', 'Pending'),
        ('doing', 'Doing'),
        ('completed', 'Completed')
    ], string="Stage", default='pending', required=True)
    material_ids = fields.One2many('sample.material', 'sample_id', string="Materials Required")
    wizard_ids = fields.One2many('sample.material.wizard', 'sample_id', string="Materials Required")
    invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True, ondelete='set null')
    invoice_generated = fields.Boolean(string="Invoice Generated", default=False, readonly=True)
    invoice_status = fields.Selection(
        selection=INVOICE_STATUS,
        string="Invoice Status",
        compute='_compute_invoice_status',
        store=True)

    total_product_quantity = fields.Float(string="Total Product Qty", compute='_compute_total_product_quantity',
                                          store=True)
    sum_of_cost = fields.Float(string="Sum Of Cost", related='total_price', store=True)
    profit = fields.Float(string="Profit", store=True, compute='_compute_profit')
    collected_payment = fields.Float(string="Collected Payment", store=True)
    balance = fields.Float(string="Balance", store=True)
    invoice_ids = fields.One2many('account.move', 'submission_id', string="Invoices")
    total_invoice_amount = fields.Float(string="Total Invoice Amount", compute='_compute_total_invoice_amount',
                                        store=True)

    def action_print_report(self, ):
        return self.env.ref('sample_submission.report_sample_submission').report_action(self)

    @api.depends('invoice_ids.amount_total')
    def _compute_total_invoice_amount(self):
        for record in self:
            print(record.total_invoice_amount, 'helo')
            record.total_invoice_amount = sum(invoice.amount_total for invoice in record.invoice_ids)

    @api.depends('total_invoice_amount', 'sum_of_cost')
    def _compute_profit(self):
        for record in self:
            record.profit = record.sum_of_cost - record.total_invoice_amount

    @api.depends('wizard_ids.quantity')
    def _compute_total_product_quantity(self):
        for record in self:
            record.total_product_quantity = sum(wizard.quantity for wizard in record.wizard_ids)

    @api.depends('stage')
    def _compute_invoice_status(self):
        if self.stage == 'completed':
            self.invoice_status = 'invoiced'
        elif self.stage == 'pending':
            self.invoice_status = 'no'
        else:
            self.invoice_status = 'to invoice'

    @api.model
    def create(self, vals):
        if vals.get('sequence', _('New')) == _('New'):
            vals['sequence'] = self.env['ir.sequence'].next_by_code('sample.submission') or _('New')
        return super(SampleSubmission, self).create(vals)

    @api.depends('price', 'discount', 'vat')
    def _compute_total_price(self):
        for record in self:
            price_after_discount = record.price - (record.price * (record.discount / 100))
            record.total_price = price_after_discount + (price_after_discount * (record.vat / 100))

    def action_generate_invoice(self):
        if self.invoice_generated:
            raise UserError(_("An invoice has already been generated for this sample submission."))

        # Create a wizard or use the existing confirmation dialog
        return {
            'name': _('Confirm Invoice Generation'),
            'type': 'ir.actions.act_window',
            'res_model': 'generate.invoice.warning',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sample_submission_id': self.id,
                'default_price': self.price,
                'default_discount': self.discount,
            }
        }

    def open_material_wizard(self):
        """Opens the material requirement wizard for adding a new material."""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Add Material Requirement',
            'res_model': 'sample.material.wizard',
            'view_mode': 'form',
            'view_id': self.env.ref('sample_submission.view_sample_material_wizard_form').id,
            'context': {'default_sample_id': self.id},
            'target': 'new',
        }

class AccountMove(models.Model):
    _inherit = 'account.move'

    # Adding the field to link an invoice to a sample submission
    submission_id = fields.Many2one('sample.submission', string="Sample Submission", ondelete='set null')
