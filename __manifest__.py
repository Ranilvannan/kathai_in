# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'kathai IN',
    'version': '1.1',
    'summary': 'Kathai',
    'sequence': 15,
    'description': 'Kathai',
    'category': 'New',
    'website': 'https://www.odoo.com/page/billing',
    'images': [],
    'depends': ['base', 'web', 'mail'],
    'data': [
        'data/kathai_in.xml',
        'security/kathai_in_security.xml',
        'security/ir.model.access.csv',
        'views/menu_view.xml',
        'views/story_view.xml',
        'views/tags_view.xml',
        'wizard/story_export.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': True,
}
