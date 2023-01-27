{
    'name': 'Custom Task Timesheet',
    'version': '1.0',
    'category': 'Services/Timesheets',
    'summary': 'Add a new type of hours field to the timesheets',
    'description': 'Add a new type of hours field to the timesheets',
    'website': 'https://www.odoo.com/page/timesheet-mobile-app',
    'depends': ['analytic', 'project', 'uom', 'timesheet_grid'],
    'data': [
        'views/project_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
