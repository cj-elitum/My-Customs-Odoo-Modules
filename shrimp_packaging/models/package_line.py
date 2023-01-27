from odoo import models, fields, api


class PackageLine(models.Model):
    _name = 'shrimp_packaging.package.line'
    _description = 'Package Line'

    package_id = fields.Many2one('shrimp_packaging.package', string="Package")
    size = fields.Float(string="Talla")
    package_type = fields.Char(string="Empaque")
    qty = fields.Float(string="Cantidad")
    weight = fields.Float(string="Peso")
    total_weight = fields.Float(string="Total")



