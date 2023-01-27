from dateutil.relativedelta import relativedelta
# Import fields and models from odoo
from odoo import fields, models, api


# A model for real estate
class Propiedad(models.Model):
    _name = 'propiedades.propiedad'  # Database table name propiedades_propiedad
    _description = 'Modelo de una propiedad en venta'  # Description when hovered

    @api.model
    def create(self, vals):
        res = super().create(vals)
        return res

    # Database fields mapped by odoo ORM
    name = fields.Char(required=True, string="Title")  # Optional parameter like required, string ,index
    description = fields.Text()
    property_type_id = fields.Many2one("propiedades.propiedad.type", string="Type")

    # These are reserved fields
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], required=True, default="new")

    postal_code = fields.Char(string="Postcode")
    date_availability = fields.Date(copy=False,
                                    default=lambda self: fields.Datetime.today() + relativedelta(months=+3),
                                    string="Available From")
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string="Garden Orientation")
