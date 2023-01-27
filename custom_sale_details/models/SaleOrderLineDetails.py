from odoo import models, fields,api


class SaleOrderLineDetails(models.Model):
    _name = 'sale.order.line.details'
    _description = 'Sale Order Line Details'
    _order = 'sale_order_int_id desc'

    sale_order_id = fields.Many2one('sale.order')
    sale_order_line_id = fields.Many2one('sale.order.line')
    # Created a new field to order based on sale order number
    sale_order_int_id = fields.Integer(compute='_compute_sale_order_int', string='Sale Order Number', store=True)
    client = fields.Many2one(related='sale_order_id.partner_id', store = True)
    product_name = fields.Many2one(string='Product', related='sale_order_line_id.product_template_id', readonly=True)
    price_unit = fields.Float(string='Unit Price', related='sale_order_line_id.price_unit', readonly=True)
    product_uom_qty = fields.Float(string='Quantity', related='sale_order_line_id.product_uom_qty', readonly=True)
    total = fields.Monetary(string='Total', related='sale_order_line_id.price_subtotal', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='sale_order_line_id.currency_id',
                                  readonly=True)

    # Executed automatically when the module is installed
    def init(self):
        existing_records = self.search([])
        if not existing_records:
            self._create_sale_order_line_details()

    # Populate the table with the data from the sale order lines
    def _create_sale_order_line_details(self):
        sale_order_line_obj = self.env['sale.order.line']
        sale_order_lines = sale_order_line_obj.search([])
        for line in sale_order_lines:
            vals = {
                'sale_order_id': line.order_id.id,
                'sale_order_line_id': line.id,
            }
            self.create(vals)

    # Create a single record for the sale order line
    def create_sale_order_line_detail(self, sale_order_line):
        vals = {
            'sale_order_id': sale_order_line.order_id.id,
            'sale_order_line_id': sale_order_line.id,
        }
        self.create(vals)


    @api.depends('sale_order_id')
    def _compute_sale_order_int(self):
        for record in self:
            if record.sale_order_id and record.sale_order_id.name.startswith('S'):
                record.sale_order_int_id = int(record.sale_order_id.name.split('S')[1])
            else:
                record.sale_order_int_id = 0