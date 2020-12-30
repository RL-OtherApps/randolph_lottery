from odoo import fields, models
from datetime import datetime


class GameData(models.Model):
    _name = "game.data"

    partner = fields.Many2one('res.partner', 'Customer')
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


class Customers(models.Model):
    _inherit = "res.partner"

    game_data = fields.One2many('game.data', 'partner', string="Game data")
    wheel_game_data = fields.One2many('game.wheel.data', 'partner', string="Wheel Game Data")
    full_name = fields.Char('Full Name')
    acc_number = fields.Char('Account Number')
    ifsc = fields.Char('IFSC')


class GameWheelData(models.Model):
    _name = "game.wheel.data"

    partner = fields.Many2one('res.partner', 'Customer')
    company = fields.Many2one('res.company', 'Company',default=lambda self: self.env.company.id)
    lottery_wheel = fields.Many2one('lottery.wheel', 'Lottery Wheel')
    input = fields.Integer('Input')
    result = fields.Integer('Result')
    amount_won = fields.Integer('Amount Won',currency_field='currency_id')
    rate = fields.Char('Rate')
    currency_id = fields.Many2one(string="Currency", related='company.currency_id', readonly=True)