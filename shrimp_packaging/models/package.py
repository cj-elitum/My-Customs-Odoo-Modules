from odoo import models, fields, api


class Package(models.Model):
    _name = 'shrimp_packaging.package'
    _description = 'Package'

    name = fields.Char(string='Name')

    cola = fields.Boolean(string="COLA")
    pcd_iqf = fields.Boolean(string="PCD IQF")
    cocido_pyd_iqf = fields.Boolean(string="COCIDO PYD IQF")
    pyd_block = fields.Boolean(string="PYD BLOQUE")
    fresh = fields.Boolean(string="FRESCOS")
    reprocesses = fields.Boolean(string="REPROCESOS")

    # Basic Info
    proccess_plant = fields.Char(string="Planta de proceso")
    provider = fields.Many2one('res.partner', string="Proveedor")
    reported_pounds = fields.Float(string="Libras reportadas")
    classified_pounds = fields.Float(string="Libras clasificadas")
    reception_date = fields.Date(string="Fecha de recepción")
    received_pounds = fields.Float(string="Libras recibidas")
    batch_number = fields.Char(string="Número de lote")

    # Packaged Product Lines
    packaged_product_lines_ids = fields.One2many('shrimp_packaging.package.line', 'package_id', string="Líneas de producto empaquetado")
    total_packaged_weight = fields.Float(string="Peso total empaquetado", compute="_compute_total_packaged_weight")

    @api.depends('packaged_product_lines_ids')
    def _compute_total_packaged_weight(self):
        for r in self:
            r.total_packaged_weight = sum(r.packaged_product_lines_ids.mapped('total_weight'))


