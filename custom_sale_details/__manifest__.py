# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sale orde details module',
    'version': '1.0',
    'category': 'Sales/Sales',
    'summary': 'Sales custom module',
    'depends': ['sale'],
    'data': [
        'views/sale_views.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'license': 'LGPL-3',
}
