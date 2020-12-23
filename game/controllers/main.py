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
        lottery = request.env['lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        if uid:
            return http.request.render('game.game_one', {'partner': uid, 'draw': lottery})
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
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
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
            'draw': lottery.id,
            'company': company.id,

        })
        return request.render('game.ticket_receipt', {'tick': game, 'receipt': company, 'draw': lottery})

    @http.route(['/report/pdf/receipt_download'], type='http', auth='public', methods=['POST'])
    def download_receipt(self, game_id):
        game_data = request.env['game.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        pdf, _ = request.env.ref('game.action_ticket_receipt').sudo()._render_qweb_pdf([int(game_data.id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'COA; filename="Receipt.pdf"')]
        return request.make_response(pdf, headers=pdfhttpheaders)
