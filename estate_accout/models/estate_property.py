from odoo import fields, models
from odoo.exceptions import UserError


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sell_property(self):
        # Create an empty account.move
        partner_id = self.buyer_id
        move_type = 'out_invoice'
        if not self.buyer_id or not self.buyer_id.property_account_receivable_id:
            raise UserError("The buyer does not have an invoice address.")

        self.env['account.move'].with_context(default_move_type=move_type).create({
            'name': 'INV/' + fields.Date.today().strftime("%Y/%m/%d"),
            'move_type': move_type,
            'partner_id': partner_id.id,
            'invoice_line_ids': [
                # 0 0 Means create a new value
                (
                    0,
                    0,
                    {
                        'quantity': 1,
                        'price_unit': self.selling_price,
                        'name': self.name
                    }
                ),
                (
                    0,
                    0,
                    {
                        'price_unit': self.selling_price * 0.06,
                        'name': 'Tax'
                    }
                ),
                (
                    0,
                    0,
                    {
                        'price_unit': 100,
                        'name': 'Administrative fees'
                    }
                ),

            ]
        })

        return super().action_sell_property()
