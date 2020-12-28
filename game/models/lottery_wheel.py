from odoo import fields, models, api, _
import random
import collections
from datetime import datetime
from odoo.exceptions import UserError


class LotteryWheel(models.Model):
    _name = "lottery.wheel"

    name = fields.Char('Name')
    player_inputs_results = fields.One2many('game.wheel.data', 'lottery_wheel', string='Players and their lottery numbers')
    rate = fields.Char('Rate')
    active_lottery = fields.Boolean('Active')
    company_id = fields.Many2one('res.company', 'company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
