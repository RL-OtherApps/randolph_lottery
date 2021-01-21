from odoo import fields, models, api
from datetime import datetime


class GameData(models.Model):
    _name = "game.data"

    partner = fields.Many2one('res.partner', 'Customer')
    agent = fields.Many2one('res.users', 'Agent')
    company = fields.Many2one('res.company', 'Company')
    draw = fields.Many2one('lottery.draw', 'Draw')
    first = fields.Integer('First')
    second = fields.Integer('Second')
    third = fields.Integer('Third')
    fourth = fields.Integer('Forth')
    fifth = fields.Integer('Fifth')
    sixth = fields.Integer('Sixth')
    create_date = fields.Datetime('Date')
    ticket_number = fields.Char('Ticket Number')
    draw_result = fields.Char('Draw Results')
    winning = fields.Char('Winning')
    winning_amount = fields.Char('Winning Amount')
    sale_order = fields.Many2one('sale.order', 'Sale Order')
    transaction_id = fields.Char('Transaction ID')


class Customers(models.Model):
    _inherit = "res.partner"

    game_data = fields.One2many('game.data', 'partner', string="Game data")
    bolet_game_data = fields.One2many('bolet.game.data', 'partner', string="Bolet Game data")
    wheel_game_data = fields.One2many('game.wheel.data', 'partner', string="Wheel Game Data")
    full_name = fields.Char('Full Name')
    acc_number = fields.Char('Account Number')
    ifsc = fields.Char('IFSC')
    customer_transactions = fields.One2many('customer.transaction', 'partner', string="Customer Transactions")
    # transactions = fields.Integer('Transaction')
    # current_wallet_amount = fields.Float('Wallet Amount', compute='calculate_wallet_amount', store=True)
    # withdraw_requests = fields.One2many('withdraw.request', 'partner', string="Withdraw Requests")

    @api.depends('customer_transactions')
    def calculate_wallet_amount(self):
        if self.customer_transactions:
            amount = 0.0
            for rec in self.customer_transactions:
                if rec.transaction_id:
                    amount = amount + rec.amount
            self.update({'current_wallet_amount': amount})
        else:
            self.update({'current_wallet_amount': 0.0})


class GameWheelData(models.Model):
    _name = "game.wheel.data"

    partner = fields.Many2one('res.partner', 'Customer')
    company = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company.id)
    lottery_wheel = fields.Many2one('lottery.wheel', 'Lottery Wheel')
    input = fields.Integer('Input')
    result = fields.Integer('Result')
    amount_won = fields.Integer('Amount Won', currency_field='currency_id')
    rate = fields.Char('Rate')
    currency_id = fields.Many2one(string="Currency", related='company.currency_id', readonly=True)
    agent = fields.Many2one('res.users', 'Agent')
    sale_order = fields.Many2one('sale.order', 'Sale Order')
    transaction_id = fields.Char('Transaction ID')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    lottery_draw = fields.Many2one('game.data', 'Lottery Draw')
    lottery_wheel = fields.Many2one('game.wheel.data', 'Lottery Wheel')
    transaction_id = fields.Char('Transaction ID')


class CustomerTransaction(models.Model):
    _name = 'customer.transaction'
    partner = fields.Many2one('res.partner', 'Customer')
    amount = fields.Float('Amount')
    transaction_id = fields.Char('Transaction Id')
    create_date = fields.Datetime('Time')


class WithdrawRequest(models.Model):
    _name = 'withdraw.request'
    partner = fields.Many2one('res.partner', 'Customer')
    amount = fields.Float('Amount')
    create_date = fields.Datetime('Time')
    status = fields.Selection([('draft', 'Draft'), ('pass', 'Passed'), ('fail', 'failed')], string='Status')
    transaction_id = fields.Char('Transaction ID')
