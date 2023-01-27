from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.model
    def create(self, vals):
        res = super(SaleOrderLine, self).create(vals)
        self.env['sale.order.line.details'].create_sale_order_line_detail(res)
        return res
