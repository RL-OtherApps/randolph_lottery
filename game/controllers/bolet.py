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
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        if uid:
            return http.request.render('game.bolet_game_template', {'draw': lottery, 'partner': uid})
        else:
            return http.request.render('web.login', )

    @http.route('/save_info_open_game', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def save_info_open_game(self, **post):
        yes = post.get('yesno')
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        agent = post.get('agent')
        agents = post.get('agents')
        customers = post.get('customers')
        if yes == "yes":
            agents = request.env['res.users'].sudo().search([('name', '=', str(agents))])
            customer = request.env['res.partner'].sudo().create({
                'name': name,
                'email': email,
                'phone': phone
            })
            return http.request.render('game.choose_game', {'customers': customer, 'agents': agents})
        else:
            customers = request.env['res.partner'].sudo().search([('name', '=', str(customers))])
            agents = request.env['res.users'].sudo().search([('name', '=', str(agent))])
            return http.request.render('game.choose_game', {'customers': customers, 'agents': agents})

    @http.route('/save_bolet_input', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def save_bolet_input(self, **post):
        partner = request.env.user.partner_id
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        l1 = post.get('l1')
        customer = post.get('partners')
        if customer:
            customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
            game = request.env['bolet.game.data'].sudo().create({
                'partner': customers.id if customers else partner.id,
                'create_date': datetime.now(),
                'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                'draw': lottery.id,
                'company': company.id,
                'agent': request.env.user.id,
                'first': l1,
            })
            return request.render('game.bolet_moncash_payment_form',
                                  {'tick': game, 'receipt': company, 'draw': lottery})
        else:
            game = request.env['bolet.game.data'].sudo().create({
                'partner': partner.id,
                'create_date': datetime.now(),
                'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                'draw': lottery.id,
                'company': company.id,
                'first': l1,
            })
            return request.render('game.bolet_moncash_payment_form',
                                  {'tick': game, 'receipt': company, 'draw': lottery})

    @http.route(['/report/pdf/bolet_receipt_download'], type='http', auth='public', methods=['POST'])
    def download_receipts(self, game_id):
        game_data = request.env['bolet.game.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        pdf, _ = request.env.ref('game.action_ticket_receipts').sudo()._render_qweb_pdf([int(game_data.id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'COA; filename="Receipt.pdf"')]
        return request.make_response(pdf, headers=pdfhttpheaders)

    @http.route('/bolet-game', type="http", auth="user", website=True)
    def pay_bolet_game(self, **post):
        uid = request.env.user.partner_id
        if uid:
            customer = post.get('customer')
            lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                return http.request.render('game.bolet_game_template', {'partners': customers, 'draw': lottery})
            else:
                return http.request.render('game.bolet_game_template', {'partners': uid, 'draw': lottery})
        else:
            return http.request.render('web.login', )

    @http.route('/open_bolet_pay', type="http", auth="user", website=True)
    def open_game1_pay(self, **post):
        partner = request.env.user.partner_id
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        customer = post.get('customers')
        amount = post.get('amount')
        amounts = post.get('amounts')
        wallet = post.get('yesno')
        if wallet == 'wallet' and amount:
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                game = request.env['bolet.game.data'].sudo().create({
                    'partner': customers.id if customers else partner.id,
                    'create_date': datetime.now(),
                    'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                    'draw': lottery.id,
                    'company': company.id,
                    'agent': request.env.user.id,
                    'betting_amount': amount
                })
                old_amount = customers.current_wallet_amount
                new_amount = old_amount - int(amount)
                customers.update({'current_wallet_amount': new_amount})
                return request.render('game.bolet_game_template', {'tick': game, 'receipt': company, 'draw': lottery})
            else:
                game = request.env['bolet.game.data'].sudo().create({
                    'partner': partner.id,
                    'create_date': datetime.now(),
                    'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                    'draw': lottery.id,
                    'company': company.id,
                    'betting_amount': amount
                })
                old_amount = partner.current_wallet_amount
                new_amount = old_amount - int(amount)
                partner.update({'current_wallet_amount': new_amount})
                return request.render('game.bolet_game_template', {'tick': game, 'receipt': company, 'draw': lottery})
        elif wallet == 'no_wallet' and amounts:
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                game = request.env['bolet.game.data'].sudo().create({
                    'partner': customers.id if customers else partner.id,
                    'create_date': datetime.now(),
                    'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                    'draw': lottery.id,
                    'company': company.id,
                    'agent': request.env.user.id,
                    'betting_amount': amounts
                })
                sale_order = self.create_sale_order(customers, amounts, game)
                lottery.update({'game_id': game.id})
                payment = self.create_payment_in_moncash(sale_order, amounts)
                game.update({'sale_order': sale_order.id})
                return request.redirect(payment)
            else:
                game = request.env['bolet.game.data'].sudo().create({
                    'partner': partner.id,
                    'create_date': datetime.now(),
                    'ticket_number': request.env['ir.sequence'].sudo().next_by_code('bolet.game.data'),
                    'draw': lottery.id,
                    'company': company.id,
                    'betting_amount': amounts
                })
                sale_order = self.create_sale_order(partner, amounts, game)
                lottery.update({'game_id': game.id})
                payment = self.create_payment_for_bolet_in_moncash(sale_order, amounts)
                game.update({'sale_order': sale_order.id})
                return request.redirect(payment)

    @http.route('/bolet_receive_payment_info', type="http", auth="user", website=True, methods=['GET', 'POST'])
    def bolet_receive_payment_info(self, **kwargs):
        transaction_id = kwargs.get('transactionId')
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        game = request.env['bolet.game.data'].sudo().search([('id', '=', int(lottery.game_id))], limit=1)
        game.update({'transaction_id': transaction_id})
        logger.warning("----------------------Request Data ======= %s ====-----------------------", kwargs)
        return request.render('game.bolet_ticket_receipt', {'tick': game, 'receipt': company, 'draw': lottery})

    def create_payment_for_bolet_in_moncash(self, order, amount):
        access_token = request.env['moncash.api'].sudo().search([('id', '=', 3)], limit=1)
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

    def create_sale_order(self, partner, amount, game):
        order = request.env['sale.order'].sudo().create({
            'partner_id': partner.id,
            'bolet_draw': game.id,
            'date_order': date.today(),
            'state': 'sale',
        })
        product_id = self.get_product_id()
        line_ids = []
        line_values = (0, 0, {
            'product_id': product_id.id,
            'name': product_id.name,
            'product_uom_qty': 1.0,
            'price_unit': float(int(amount))
        })
        line_ids.append(line_values)
        order.write({'order_line': line_ids})
        return order

    def get_product_id(self):
        product_id = request.env['product.product'].sudo().search([('name', '=', 'Transaction Amount')])
        if product_id:
            return product_id
        else:
            new_product_id = request.env['product.product'].sudo().create({
                'name': 'Transaction Amount',
            })
            return new_product_id

    @http.route('/open_bolet_payment', type="http", auth="user", website=True)
    def open_bolet_payment(self, **post):
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['bolet.lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        amount = post.get('amount')
        amounts = post.get('amounts')
        tick = post.get('tick')
        wallet = post.get('yesno')
        if wallet == 'wallet' and amount:
            bolet_game = request.env['bolet.game.data'].sudo().search([('id', '=', int(tick))])
            if float(int(amount)) <= bolet_game.partner.current_wallet_amount:
                bolet_game.update({'betting_amount': amount})
                old_amount = bolet_game.partner.current_wallet_amount
                new_amount = old_amount - int(amount)
                bolet_game.partner.update({'current_wallet_amount': new_amount})
                return request.render('game.bolet_ticket_receipt',
                                      {'tick': bolet_game, 'receipt': company, 'draw': lottery})
            else:
                return request.render('game.wallet_sorry_page')
        elif wallet == 'no_wallet' and amounts:
            bolet_game = request.env['bolet.game.data'].sudo().search([('id', '=', int(tick))])
            bolet_game.update({'betting_amount': amounts})
            sale_order = self.create_sale_order(bolet_game.partner, amounts, bolet_game)
            lottery.update({'game_id': bolet_game.id})
            payment = self.create_payment_for_bolet_in_moncash(sale_order, amounts)
            bolet_game.update({'sale_order': sale_order.id})
            return request.redirect(payment)
