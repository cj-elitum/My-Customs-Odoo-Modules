from datetime import timedelta
from odoo import fields, models, api
from odoo.exceptions import ValidationError


# A class that models property offers
class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offers from potential buyers"
    _order = "price desc"

    # def write(self, vals):
    #     if 'status' in vals and vals.get('status') == 'accepted':
    #         for offer in self:
    #             offer.property_ids.write({'selling_price': offer.price})
    #     return super().write(vals)

    price = fields.Float(required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_ids = fields.Many2one("estate.property", required=True, ondelete='cascade')
    # Add a related field that points to the property types id
    property_type_id = fields.Many2one(related="property_ids.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    # SQL constraints
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'The price should be positive')
    ]

    @api.model
    def create(self, vals_list):
        # Check if the price of the offer is more than other offers
        if 'property_ids' in vals_list:
            offers = self.search([('property_ids', '=', vals_list['property_ids'])])
            if offers:
                if vals_list['price'] <= max(offers.mapped('price')):
                    raise ValidationError("Cannot create offer: the price should be higher than the other offers")

        # When an offer is created modify the property state to offer_received
        res = super().create(vals_list)
        res.property_ids.write({'state': 'offer_received'})
        return res

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                # Set the date to today if the offer is new
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            rd = offer.date_deadline - fields.Date.today()
            offer.validity = rd.days

    def action_confirm(self):
        for offer in self:
            # Check if there are other accepted offers first
            accepted_offers = self.search([
                ('property_ids', '=', offer.property_ids.id),
                ('status', '=', 'accepted'),
                ('id', '!=', offer.id),
            ])

            if not accepted_offers:
                offer.status = "accepted"
                offer.property_ids.write({
                    'selling_price': offer.price,
                    'buyer_id': offer.partner_id,
                    'state': 'offer_accepted',
                })
            else:
                raise ValidationError("Cannot accept offer: another offer has already been accepted for this property")

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"







