from odoo import models, fields, api


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = 'Product Brand'
    _order = 'name'

    name = fields.Char(string='Brand', required=True)
    description = fields.Text(string='Description')
    product_ids = fields.One2many('product.template', 'brand_id', string='Products')
