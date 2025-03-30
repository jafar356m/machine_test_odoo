from odoo import models, fields, api

class SampleSubmissionReportWizard(models.TransientModel):
    _name = 'sample.submission.report.wizard'
    _description = 'Sample Submission Report Wizard'

    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    submission_ids = fields.Many2many('sample.submission', string='submission')

    def generate_excel_report(self):
        # Fetch sample submissions based on the date range
        submissions = self.env['sample.submission'].search([
            ('submission_date', '>=', self.date_from),
            ('submission_date', '<=', self.date_to)
        ])
        data = {
            'submission_ids': submissions.ids,  # Pass IDs to the report
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        # Trigger Excel report
        return self.env.ref('sample_submission.sample_submission_excel_report').report_action(self, data=data)
    def generate_pdf_report(self):
        data = {
            'submission_ids': self.submission_ids.ids,  # Pass IDs to the report
            'date_from': self.date_from,
            'date_to': self.date_to,
        }
        print(data,'data')
        return self.env.ref('sample_submission.report_sample_submission_date').report_action(self, data=data)



class OpenAcademyReportPDF(models.AbstractModel):
    _name = 'report.sample_submission.sample_submission_pdf_report_pdf'

    def _get_report_values(self, docids, data=None):
        domain=[]
        if data.get('date_from'):
            domain.append(('submission_date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('submission_date', '<=', data.get('date_to')))
        if data.get('submission_ids'):
            domain.append(('id', 'in', data.get('submission_ids')))

        docs = self.env['sample.submission'].search(domain)

        company = self.env['res.company'].search([], limit=1)
        print(company,'docs')
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sample.submission',
            'docs': docs,
            'company': company,  # Pass the company data to be accessible in the template
            'datas': data
        }
