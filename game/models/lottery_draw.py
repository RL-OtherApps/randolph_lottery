from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import UserError


class LotteryDraw(models.Model):
    _name = "lottery.draw"

    name = fields.Char('Name')
    draw_time = fields.Datetime('Draw Time')
    active_draw = fields.Boolean('Active')
    player_inputs = fields.One2many('game.data', 'draw', string='Players and their lottery numbers')

    # @api.onchange('active_draw')
    # def check_active(self):
    #     for item in self:
    #         if not item.active_draw:
    #             lottery = self.env['lottery.draw'].sudo().search([('active_draw', '=', True)])
    #             if not lottery:
    #                     item.active_draw = True
    #             else:
    #                 raise UserError(_('One draw is already activated'))
    #         else:
    #             pass
