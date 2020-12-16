# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class GameLoader(http.Controller):

    @http.route('/first-game', type="http", auth="user", website=True)
    def play_first_game(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.game_one',{})
        else:
            return http.request.render('web.login', {})

    @http.route('/second-game', type="http", auth="user", website=True)
    def play_second_game(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.game_two', {})
        else:
            return http.request.render('web.login', {})