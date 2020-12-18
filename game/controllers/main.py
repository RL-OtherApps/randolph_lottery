# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
from datetime import datetime

_logger = logging.getLogger(__name__)


class GameLoader(http.Controller):

    @http.route('/first-game', type="http", auth="user", website=True)
    def play_first_game(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.game_one', {'partner': uid})
        else:
            return http.request.render('web.login', )

    @http.route('/second-game', type="http", auth="user", website=True)
    def play_second_game(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.game_two', {})
        else:
            return http.request.render('web.login', {})

    @http.route('/save_numbers', auth='public', type='http', website=True, methods=['POST'])
    def save_numbers(self, l1, l2, l3, l4, l5, l6):
        partner = request.env.user.partner_id
        company = request.env['res.company'].sudo().search([('name', '=', 'YourCompany')])
        game = request.env['game.data'].sudo().create({
            'partner': partner.id,
            'create_date': datetime.now(),
            'ticket_number': request.env['ir.sequence'].sudo().next_by_code('game.data'),
            'first': l1,
            'second': l2,
            'third': l3,
            'fourth': l4,
            'fifth': l5,
            'sixth': l6,
        })
        return request.render('game.ticket_receipt', {'tick': game, 'receipt': company})
        # return http.request.redirect('/login')
