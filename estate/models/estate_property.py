from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


# This is our estate property model
# Odoo ORM will create a database table for this model
class EstateProperty(models.Model):
    # This is the name of the table that will be created in the database
    # The name of the table will be estate_property
    _name = "estate.property"
    _description = "Real state properties"
    _order = "id desc"

    # A Many 2 one relationship with the estate.property.type model
    # Points to the estate.property.type model, acts like a foreign key
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    # Adding a buyer to the property, using a reference to res.partner model
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    salesman_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.uid)

    # A many 2 many relationship with the estate.property.tag model
    tag_ids = fields.Many2many(comodel_name='estate.property.tag',
                               relation='estate_property_tag_rel',
                               column1='property_id',
                               column2='tag_id',
                               string='Tags')

    # A one 2 many relationship with the estate.property.offer model
    offer_ids = fields.One2many(comodel_name='estate.property.offer',
                                inverse_name='property_ids',
                                string='Offers')

    # These are reserved fields in Odoo
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
    ], default='new')

    # These are the fields that we defined
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=lambda self: fields.Datetime.today() + relativedelta(months=+3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    # A selection field contains a list of tuples, appears as a dropdown in the UI
    garden_orientation = fields.Selection([('north', 'North'),
                                           ('south', 'South'),
                                           ('east', 'East'),
                                           ('west', 'West')])

    # A computed field, it's value is computed based on other fields
    total_area = fields.Integer(compute='_compute_total_area')
    best_price = fields.Float(compute='_compute_best_price')

    # SQL constraints
    _sql_constraints = [
        ('check_expected_price', 'CHECK(expected_price > 0)',
         'The price should be positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'The selling price should be positive'),
    ]

    def unlink(self):
        for estate_property in self:
            # Only properties with anew or canceled state can be deleted
            if estate_property.state not in ['new', 'canceled']:
                raise UserError("Only new or canceled properties can be deleted")
        return super(EstateProperty, self).unlink()

    @api.constrains('selling_price')
    def _check_selling_price(self):
        expected_price_threshold = 0.9
        min_accepted_price = expected_price_threshold * self.expected_price if self.expected_price else 0
        for estate_property in self:
            if estate_property.selling_price < min_accepted_price:
                raise ValidationError("The selling price is too low")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for estate_property in self:
            estate_property.total_area = estate_property.garden_area + estate_property.living_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for estate_property in self:
            if estate_property.offer_ids:
                estate_property.best_price = max(estate_property.offer_ids.mapped('price'))
            else:
                estate_property.best_price = 0

    # Onchange changes fields depending on a specified field
    #  we do not loop on self, this is because the method
    #  is only triggered in a form view, where self is always a single record.
    @api.onchange("garden")
    def _onchange_partner_id(self):
        self.garden_area = 10 if self.garden else 0
        self.garden_orientation = "north" if self.garden else ""

    # Change status depending on if we received an offer
    # @api.onchange("offer_ids")
    # def _onchange_offer_ids(self):
    #     if self.offer_ids:
    #         self.state = "offer_received"
    #     else:
    #         self.state = "new"

    def action_cancel_property(self):
        for estate_property in self:
            if estate_property.state != "sold":
                estate_property.state = "canceled"
            else:
                raise UserError("Sold properties cannot be canceled")

    def action_sell_property(self):
        for estate_property in self:
            if estate_property.state != "canceled":
                estate_property.state = "sold"
            else:
                raise UserError("Canceled properties cannot be sold")

