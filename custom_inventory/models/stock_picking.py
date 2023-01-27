from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Add a new field to the model
    origin_link = fields.Char(string="Document Link", compute='_compute_origin_link')

    #Lets create an invisible field that we will use to store if origin is available or not
    origin_available = fields.Boolean(compute='_compute_origin_available')

    @api.depends('origin')
    def _compute_origin_available(self):
        for picking in self:
            if picking.origin:
                sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                if sale_order:
                    picking.origin_available = True
                else:
                    picking.origin_available = False
            else:
                picking.origin_available = False

    @api.depends('origin')
    def _compute_origin_link(self):
        # Origin is a char field, so we can't use it to link to the document
        # We need to find the document based on the origin name
        for picking in self:
            if picking.origin:
                # Find the sale order
                sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                if sale_order:
                    # Get the URL to the sale order
                    picking.origin_link = '<a href="/web#id=%s&view_type=form&model=sale.order" target="_blank">%s</a>' % (
                        sale_order.id, picking.origin)
                    # Other way to do it:
                    # web_link = self.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/web#id=' + str(sale_order.id) + '&view_type=form&model=sale.order'
                    # picking.origin_link = '<a href="' + web_link + '" target="_blank">' + picking.origin + '</a>'
                else:
                    picking.origin_link = picking.origin
            else:
                picking.origin_link = ''

    def open_sale_order(self):
        for picking in self:
            if picking.origin:
                # Find the sale order
                sale_order = self.env['sale.order'].search([('name', '=', picking.origin)], limit=1)
                if sale_order:
                    # Open the sale order
                    return {
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'sale.order',
                        'res_id': sale_order.id,
                    }
        return False



