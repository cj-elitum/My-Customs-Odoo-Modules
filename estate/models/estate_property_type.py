from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


# A class that models a property type
class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Property types"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.One2many(comodel_name='estate.property',
                                   inverse_name='property_type_id',
                                   string='Properties')
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute='_compute_total_offers')
    sequence = fields.Integer(default=1)

    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'The type must be unique'),
    ]

    @api.depends('offer_ids')
    def _compute_total_offers(self):
        # Get the total number of offers for each property type
        for record in self:
            record.offer_count = len(record.offer_ids)

