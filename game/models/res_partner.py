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


class Customers(models.Model):
    _inherit = "res.partner"

    game_data = fields.One2many('game.data', 'partner', string="Game data")
