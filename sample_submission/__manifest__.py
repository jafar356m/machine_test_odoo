{
    'name': 'Sample Submission',
    'version': '1.0',
    'category': 'Custom',
    'summary': 'Module for managing sample submissions',
    'description': """
        A module to track and manage sample submissions, including details like sample type, client, submission date, and status.
    """,
    'author': 'Jafar',
    'website': 'https://yourwebsite.com',
    'license': 'LGPL-3',
    'depends': ['account', 'report_xlsx'],  # add other modules if needed
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'reports/sample_submission_report.xml',
        'reports/sample_submission_pdf_report.xml',
        'reports/report_sample_submission_date_wizard.xml',
        'wizard/sample_submission_report_wizard.xml',
        'wizard/sample_material_wizard_views.xml',
        'wizard/generate_invoice_wizard_views.xml',
        'views/res_partner.xml',
        'views/sample_submission_views.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'sample_submission/static/description/watermark.png',
        ],
    },
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
