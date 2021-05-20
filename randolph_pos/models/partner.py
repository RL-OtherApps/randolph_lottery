from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    transaction_id = fields.Char('Transaction ID')


class PosConfig(models.Model):
    _inherit = 'pos.config'
    _description = 'Point of Sale Configuration'

    display_use_wallet = fields.Boolean(string='Use Moncash Wallet',
                                        help="User can user moncash wallet method for payment")

    display_natcash = fields.Boolean(string='Use NatCash Pay')
    display_moncash = fields.Boolean(string='Use Moncash Pay')
