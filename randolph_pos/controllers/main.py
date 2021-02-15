# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
import werkzeug.utils

from datetime import datetime, date
import requests
import json

logger = logging.getLogger(__name__)


class MoncashPos(http.Controller):

    @http.route('/pay_amount_via_moncash', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def pay_amount_via_moncash(self, **post):
        uid = request.env.user.partner_id
        order = post.get('order')
        total = post.get('total_amount')
        payment = self.create_payment_for_bolet_in_moncash(order, total)
        values = {}
        values.update({'payment_url': payment})
        return json.dumps(values)

    def create_payment_for_bolet_in_moncash(self, order, amount):
        access_token = request.env['moncash.api'].sudo().search([('id', '=', 4)], limit=1)
        token = access_token.get_auth_token()
        if token:
            url = "https://sandbox.moncashbutton.digicelgroup.com/Api/v1/CreatePayment"
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
            }
            data_val = {"amount": str(amount), "orderId": str(order)}
            data = json.dumps(data_val)
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 202:
                content = json.loads(response.content.decode('utf-8'))
                refresh_token = content.get('payment_token').get('token')
                redirect_url = "https://sandbox.moncashbutton.digicelgroup.com/Moncash-middleware/Payment/Redirect?token=%s" % refresh_token
                return redirect_url

    @http.route('/pos_receive_payment_info', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def pos_receive_payment_info(self, **kwargs):
        if kwargs.get('transactionId'):
            transaction_id = kwargs.get('transactionId')
            values = {}
            values.update({'transaction_id': transaction_id})
            return json.dumps(values)
        else:
            pass