# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
from datetime import datetime, date
import requests
import json

logger = logging.getLogger(__name__)


class Bolet(http.Controller):

    @http.route('/bolet_game', type="http", auth="user", website=True)
    def choose_user(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.bolet_game_template')
        else:
            return http.request.render('web.login', )

    @http.route('/save_bolet_input', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def save_bolet_input(self, **post):
        partner = request.env.user.partner_id
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        l1 = post.get('l1')
        game = request.env['bolet.game.data'].sudo().create({
            'partner': partner.id,
            'first': l1,
            'create_date': datetime.now(),
            'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
            'draw': lottery.id,
            'company': company.id,
            'agent': request.env.user.id
        })
        return http.request.render('game.thanks_page')
