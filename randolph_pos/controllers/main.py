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

    @http.route('/pos_receive_payment_info', type="http", auth="public", website=True, methods=['GET', 'POST'],
                csrf=False)
    def pos_receive_payment_info(self, **kwargs):
        uid = request.env.user.partner_id
        if kwargs.get('transactionId'):
            transaction_id = kwargs.get('transactionId')
            uid.update({'transaction_id': transaction_id})

    @http.route('/get_transaction_id', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_transaction_id(self, **post):
        uid = request.env.user.partner_id
        transaction_id = uid.transaction_id
        values = {}
        values.update({'transaction_id': transaction_id})
        return json.dumps(values)

    @http.route('/clear_transaction_id', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def clear_transaction_id(self, **post):
        uid = request.env.user.partner_id
        uid.update({'transaction_id': ''})

    @http.route('/get_wallet_amount', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_wallet_amount(self, **post):
        customer = post.get('customer')
        comp = request.env.company
        if customer:
            customer_id = request.env['res.partner'].sudo().search([('name', '=', str(customer))], limit=1)
            values = {}
            values.update({'customer': customer_id.current_wallet_amount, 'curr': comp.currency_id.symbol})
            return json.dumps(values)

    @http.route('/pay_with_wallet', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def pay_with_wallet(self, **post):
        customer = post.get('customer')
        amount = post.get('amount')
        new_amounts = 0.0
        if amount:
            new_amounts = float(amount)
        status = ''
        if customer:
            customer_id = request.env['res.partner'].sudo().search([('name', '=', str(customer))], limit=1)
            if customer_id:
                if new_amounts <= customer_id.current_wallet_amount:
                    new_amount = customer_id.current_wallet_amount - new_amounts
                    customer_id.update({'current_wallet_amount': new_amount})
                    status = "All OK"
                else:
                    status = "Not OK"
        values = {}
        values.update({'status': status})
        return json.dumps(values)

    @http.route('/get_lotto_games', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_lotto_games(self, **post):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url + '/choose_users'
        values = {}
        values.update({'url': url})
        return json.dumps(values)

    @http.route('/get_wallet_recharge', auth='public', type='http', website=True, methods=['POST'], csrf=False)
    def get_wallet_recharge(self, **post):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url + '/open_payment_wallet'
        values = {}
        values.update({'url': url})
        return json.dumps(values)
