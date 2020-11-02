# -*- coding: utf-8 -*-
{
    'name': "Timesheet begin and end",

    'summary': """Add begin and end times to timesheets.""",

    'description': """
    """,

    'author': "glueckkanja-gab AG",
    'website': "https://www.glueckkanja-gab.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Timesheet',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_timesheet'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
        'views/hr_timesheet_beginend.xml'       
    ],
    # only loaded in demonstration mode
    'demo': [
 #       'demo.xml',
    ],
}
