{
    'name': 'crm_management',
    'summary': 'lead management',
    'description': """Lead Management""",
    'website': "https://www.yourcompany.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['sale', 'mail', 'hr'],
    # always loaded
    'data': ['security/ir.model.access.csv',
             'data/data.xml',
             'views/management_patient_view.xml',
             'views/manager_view.xml',
             'views/management_appointment_view.xml',
             # 'views/age_view.xml',
             # 'views/patient_gender_view.xml',
             'views/sale.xml',
             'report/patient_detail_template.xml',
             'report/report.xml',
             ],
    # only loaded in demonstration mode
    'demo': [],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
}