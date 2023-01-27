from odoo import fields, models, api


# A model for real estate
class PropiedadTypes(models.Model):
    _name = 'propiedades.propiedad.type'  # Database table name propiedades_propiedad
    _description = 'Modela el tipo o categoria de una propiedad en venta'  # Description when hovered

    # Database fields mapped by odoo ORM
    name = fields.Char(required=True)



