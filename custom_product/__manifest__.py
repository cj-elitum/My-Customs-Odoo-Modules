{
    'name': 'Custom Product',
    'version': '1.0',
    'category': 'Sales/Sales',
    'depends': ['base', 'mail', 'uom', 'product', 'stock'],
    'description': "Custom Module that add new feature to product model",
    'data': [
        'views/stock_menu_product_views.xml',
        'views/product_template_view.xml',
        'security/ir.model.access.csv',
        'reports/custom_sale_order_report_templates.xml',
        'reports/custom_sale_order_reports.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
