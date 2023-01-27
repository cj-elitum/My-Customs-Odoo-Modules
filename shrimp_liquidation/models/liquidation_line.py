from odoo import models, fields, api


class LiquidationLine(models.Model):
    _name = 'shrimp_liquidation.liquidation.line'
    _description = 'Package Line'

    liquidation_id = fields.Many2one('shrimp_liquidation.liquidation', string="Liquidacion")
    product_template_id = fields.Many2one('product.template', string="Producto")

    package_type = fields.Char(string="Empaque")
    qty = fields.Float(string="Cantidad")
    weight = fields.Float(string="Peso")
    total_weight = fields.Float(string="Total")



