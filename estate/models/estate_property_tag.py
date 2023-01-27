from odoo import fields, models


# A class that models property tags
class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Properties tags"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.Many2many(comodel_name='estate.property',
                                    relation='estate_property_tag_rel',
                                    column1='tag_id',
                                    column2='property_id',
                                    string='Properties')
    color = fields.Integer()


    # SQL constraints
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)',
         'The type must be unique'),
    ]
