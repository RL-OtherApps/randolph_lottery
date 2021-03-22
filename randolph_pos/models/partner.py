from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    transaction_id = fields.Char('Transaction ID')
