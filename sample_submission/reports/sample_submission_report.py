from odoo import models
from datetime import datetime

class SampleSubmissionXlsxReport(models.AbstractModel):
    _name = 'report.sample_submission.sample_submission_excel_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, wizard):
        submissions = self.env['sample.submission'].browse(data['submission_ids'])

        # Create an Excel worksheet
        sheet = workbook.add_worksheet("Sample Submissions")

        # Title format
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 14,
            'align': 'center'
        })

        # Write the title in the first row and merge cells for title
        title = f"Sample Submission Report ({data['date_from']} to {data['date_to']})"
        sheet.merge_range('A1:J1', title, title_format)  # Adjust column range (A to J) based on headers

        # Set up the column headers format
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})

        # Write headers to the Excel sheet starting from row 2 (index 1)
        headers = ["Sl No", "Sample Sequence Number", "Name of Sample", "Customer", "Date of Submission", "Description", "Price", "Discount", "VAT", "Stage"]
        for col_num, header in enumerate(headers):
            sheet.write(2, col_num, header, header_format)  # Start headers from row 3 in Excel (index 2)

        # Set column widths for readability
        column_widths = [8, 20, 25, 20, 15, 30, 10, 10, 10, 15]
        for i, width in enumerate(column_widths):
            sheet.set_column(i, i, width)

        # Write data rows starting from row 4 (index 3)
        row = 3
        for idx, submission in enumerate(submissions, start=1):
            sheet.write(row, 0, idx)  # Serial number
            sheet.write(row, 1, submission.sequence)
            sheet.write(row, 2, submission.name)
            sheet.write(row, 3, submission.customer_id.name)
            sheet.write(row, 4, submission.submission_date.strftime('%Y-%m-%d') if submission.submission_date else '')
            sheet.write(row, 5, submission.description)
            sheet.write(row, 6, submission.price)
            sheet.write(row, 7, submission.discount)
            sheet.write(row, 8, submission.vat)
            sheet.write(row, 9, submission.stage)
            row += 1
