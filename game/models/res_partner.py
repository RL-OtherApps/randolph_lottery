from odoo import fields, models


class GameData(models.Model):
    _name = "game.data"

    partner = fields.Many2one('res.partner', 'Customer')
    first = fields.Integer('First')
    second = fields.Integer('Second')
    third = fields.Integer('Third')
    fourth = fields.Integer('Forth')
    fifth = fields.Integer('Fifth')
    sixth = fields.Integer('Sixth')


class Customers(models.Model):
    _inherit = "res.partner"

    game_data = fields.One2many('game.data', 'partner', string="Game data")