from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    # Add a new selection field to the timesheets, with the new type of hours
    type_hours = fields.Selection([
        ('warranty_hours', 'Horas de garantia'),
        ('normal_hours', 'Horas normales')
    ], default='normal_hours')



