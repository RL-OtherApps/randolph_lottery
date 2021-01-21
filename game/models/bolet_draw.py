from odoo import fields, models, api, _
import random
import collections
from datetime import datetime
from odoo.exceptions import UserError


class BoletLotteryDraw(models.Model):
    _name = "bolet.lottery.draw"

    name = fields.Char('Name')
    draw_time = fields.Datetime('Draw Time')
    active_draw = fields.Boolean('Active')
    player_inputs = fields.One2many('bolet.game.data', 'draw', string='Players and their lottery numbers')
    first = fields.Integer('First')
    second = fields.Integer('Second')
    third = fields.Integer('Third')
    draw_generated = fields.Boolean('Draw Generated?')
    first_prize = fields.Integer('First Digit', currency_field='currency_id')
    second_prize = fields.Integer('Front Pair', currency_field='currency_id')
    third_prize = fields.Integer('Back Pair', currency_field='currency_id')
    rate = fields.Char('Rate')
    company_id = fields.Many2one('res.company', 'company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    game_id = fields.Integer('Game ID')

    def generate_numbers(self):
        res = []
        n = 6
        for j in range(n):
            res.append(random.randint(1, 49))
        self.first = res[0]
        self.second = res[1]
        self.third = res[2]
        self.fourth = res[3]
        self.fifth = res[4]
        self.sixth = res[5]
        self.draw_generated = True


class BoletGameData(models.Model):
    _name = "bolet.game.data"

    partner = fields.Many2one('res.partner', 'Customer')
    agent = fields.Many2one('res.users', 'Agent')
    company = fields.Many2one('res.company', 'Company')
    draw = fields.Many2one('bolet.lottery.draw', 'Draw')
    first = fields.Integer('First')
    create_date = fields.Datetime('Date')
    ticket_number = fields.Char('Ticket Number')
    draw_result = fields.Char('Draw Results')
    winning = fields.Char('Winning')
    winning_amount = fields.Char('Winning Amount')
    sale_order = fields.Many2one('sale.order', 'Sale Order')
    transaction_id = fields.Char('Transaction ID')
