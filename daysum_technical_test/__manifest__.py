# -*- coding: utf-8 -*-
{
    'name': "Odoo Daysum Technical Test",

    'summary': """
        Customisations to invoicing app""",

    'description': """
        Customisations to invoicing app
    """,

    'author': "Onuh Victor",
    'website': "https://github.com/onuh",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Invoicing',
    'version': '16.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['account'],

    # always loaded
    'data': ['views/views.xml'],
    'assets': {
        'web.assets_backend': [
            'daysum_technical_test/static/src/views/**/*',
        ],
    },
    # only loaded in demonstration mode
    'demo': [],
     'installable': True,
    'application': True,
}
