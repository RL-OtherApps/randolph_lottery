# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
from datetime import datetime, date
import requests
import json

logger = logging.getLogger(__name__)


class GameLoaderTwo(http.Controller):

    @http.route('/second-game', type="http", auth="user", website=True)
    def play_second_game(self, **post):
        uid = request.env.user.partner_id
        if uid:
            customer = post.get('customer')
            lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                return http.request.render('game.moncash_payment_form_two', {'partner': customers, 'lottery': lottery})
            else:
                return http.request.render('game.moncash_payment_form_two', {'partners': uid, 'lottery': lottery})
        else:
            return http.request.render('web.login', )

    @http.route('/open_game2_pay', type="http", auth="user", website=True)
    def open_game2_pay(self, amount, **post):
        partner = request.env.user.partner_id
        lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
        customer = post.get('customers')
        if customer:
            customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
            game_wheel = request.env['game.wheel.data'].sudo().create({
                'partner': customers.id if customers else partner.id,
                'create_date': datetime.now(),
                'lottery_wheel': lottery.id,
                'rate': lottery.rate,
                'agent': request.env.user.id,
                'company': lottery.company_id.id,
            })
            sale_order = self.create_sale_order(customers, amount, game_wheel)
            lottery.update({'game_id': game_wheel.id})
            payment = self.create_payment_in_moncash2(sale_order, amount)
            game_wheel.update({'sale_order': sale_order.id})
            # sale_order.update({'transaction_id': payment})
            return request.redirect(payment)
        else:
            game_wheel = request.env['game.wheel.data'].sudo().create({
                'partner': partner.id,
                'create_date': datetime.now(),
                'lottery_wheel': lottery.id,
                'rate': lottery.rate,
                'company': lottery.company_id.id,
            })
            sale_order = self.create_sale_order(partner, amount, game_wheel)
            lottery.update({'game_id': game_wheel.id})
            payment = self.create_payment_in_moncash2(sale_order, amount)
            game_wheel.update({'sale_order': sale_order.id})
            # sale_order.update({'transaction_id': payment})
            return request.redirect(payment)

    @http.route('/open_game', auth='public', type='http', website=True, methods=['GET', 'POST'])
    def open_second_game(self, input_number, **post):
        partner = request.env.user.partner_id
        lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
        game_wheel = request.env['game.wheel.data'].sudo().search([('id', '=', int(lottery.game_id))], limit=1)
        game_wheel.sudo().update({
            'input': input_number
        })
        return http.request.render('game.game_two', {'game': game_wheel})

    @http.route('/get_result_game_two', auth='public', type='http', website=True, methods=['GET', 'POST'])
    def save_result_game_two(self, result_number, game_id):
        game_data = request.env['game.wheel.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        if int(game_data.input) == int(result_number):
            amount = int(result_number) * int(game_data.rate)
            game_data.update({'result': result_number, 'amount_won': amount, 'company': company})
            values = {'game': game_data}
            return http.request.render('game.claim_button_page2', values)
        else:
            game_data.update({'result': result_number, 'amount_won': 0, 'company': company})
            return http.request.render('game.thanks_page', {})

    @http.route('/claim_prize_two', type='http', auth="user", methods=['GET', 'POST'], website=True,
                csrf=False)
    def claim_prize_game_two(self, game_id, **post):
        game_data = request.env['game.wheel.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        partner = request.env.user.partner_id
        name = post.get('name')
        acc_number = post.get('acc_number')
        ifsc = post.get('ifsc')
        values = {'game_data': game_data}
        if name and acc_number and ifsc:
            partner.update({
                'full_name': name,
                'acc_number': acc_number,
                'ifsc': ifsc,
            })
            product_id = request.env['product.product'].sudo().search([('name', '=', 'Lottery Wheel Winner')])
            journal = request.env['account.journal'].sudo().search([('name', '=', 'Vendor Bills')], limit=1)
            if product_id:
                vals = {
                    'partner_id': partner.id,
                    'journal_id': journal.id,
                    'invoice_date': date.today(),
                    'date': date.today(),
                    'move_type': "in_invoice",
                    'state': 'draft'
                }
                bills = request.env['account.move'].sudo().create(vals)
                line_ids = []
                line_values = (0, 0, {
                    'product_id': product_id.id,
                    'name': product_id.name,
                    'quantity': 1,
                    'price_unit': float(int(game_data.amount_won))
                })
                line_ids.append(line_values)
                bills.write({'invoice_line_ids': line_ids})
            else:
                product_id = request.env['product.product'].sudo().create({
                    'name': 'Lottery Wheel Winner',
                })
                if product_id:
                    vals = {
                        'partner_id': partner.id,
                        'journal_id': journal.id,
                        'invoice_date': date.today(),
                        'date': date.today(),
                        'move_type': "in_invoice",
                        'state': 'draft'
                    }
                    bills = request.env['account.move'].sudo().create(vals)
                    line_ids = []
                    line_values = (0, 0, {
                        'product_id': product_id.id,
                        'name': product_id.name,
                        'quantity': 1,
                        'price_unit': float(int(game_data.amount_won))
                    })
                    line_ids.append(line_values)
                    bills.write({'invoice_line_ids': line_ids})
        return request.render('game.thanks_page', {})

    @http.route('/create_payment_in_moncash2', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def create_payment_in_moncash2(self, order, amount):
        access_token = request.env['moncash.api'].sudo().search([('id', '=', 2)], limit=1)
        token = access_token.get_auth_token()
        if token:
            url = "https://sandbox.moncashbutton.digicelgroup.com/Api/v1/CreatePayment"
            headers = {
                "accept": "application/json",
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json",
            }
            data_val = {"amount": str(amount), "orderId": str(order.id)}
            data = json.dumps(data_val)
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 202:
                content = json.loads(response.content.decode('utf-8'))
                refresh_token = content.get('payment_token').get('token')
                redirect_url = "https://sandbox.moncashbutton.digicelgroup.com/Moncash-middleware/Payment/Redirect?token=%s" % refresh_token
                return redirect_url
