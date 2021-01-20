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