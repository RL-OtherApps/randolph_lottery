# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)


class GameLoader(http.Controller):

    @http.route('/choose_users', type="http", auth="user", website=True)
    def choose_user(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.choose_user')
        else:
            return http.request.render('web.login', )

    @http.route('/open_as_customer', type="http", auth="user", website=True)
    def choose_game(self, **kwargs):
        uid = request.env.user.partner_id
        if uid:
            return http.request.render('game.choose_game')
        else:
            return http.request.render('web.login', )

    @http.route('/open_as_agent', type="http", auth="user", website=True)
    def reg_customer(self, **kwargs):
        customers = request.env['res.partner'].sudo().search([])
        agents = request.env['res.users'].sudo().search([])
        return http.request.render('game.reg_customer', {'customers': customers, 'agents': agents})

    @http.route('/save_info_open_game', type="http", auth="user", website=True, methods=['POST'])
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

    # -----------------Functions of first game-------------

    @http.route('/first-game', type="http", auth="user", website=True)
    def play_first_game(self, **post):
        uid = request.env.user.partner_id
        if uid:
            customer = post.get('customer')
            lottery = request.env['lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                return http.request.render('game.game_one', {'partner': customers, 'draw': lottery})
            else:
                return http.request.render('game.game_one', {'partners': uid, 'draw': lottery})

        else:
            return http.request.render('web.login', )

    @http.route('/save_numbers', auth='public', type='http', website=True, methods=['POST'])
    def save_numbers(self, l1, l2, l3, l4, l5, l6, **post):
        partner = request.env.user.partner_id
        company = request.env['res.company'].sudo().search([('name', '=', 'Ydnar Lottery')])
        lottery = request.env['lottery.draw'].sudo().search([('active_draw', '=', True)], limit=1)
        customer = post.get('customers')
        if customer:
            customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
            game = request.env['game.data'].sudo().create({
                'partner': customers.id if customers else partner.id,
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
                'agent': request.env.user.id
            })
            return request.render('game.moncash_button', {'tick': game, 'receipt': company, 'draw': lottery})
        else:
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
            return request.render('game.moncash_button', {'tick': game, 'receipt': company, 'draw': lottery})

    @http.route('/claim_prize/<string:id>', type='http', auth="user", methods=['GET'], website=True,
                csrf=False)
    def contract_details(self, id, **post):
        game_data = request.env['game.data'].sudo().search([('id', '=', int(id))], limit=1)
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
            product_id = request.env['product.product'].sudo().search([('name', '=', 'Lottery Draw Winner')])
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
                    'price_unit': float(int(game_data.winning_amount))
                })
                line_ids.append(line_values)
                bills.write({'invoice_line_ids': line_ids})
            else:
                product_id = request.env['product.product'].sudo().create({
                    'name': 'Lottery Draw Winner',
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
                        'price_unit': float(int(game_data.winning_amount))
                    })
                    line_ids.append(line_values)
                    bills.write({'invoice_line_ids': line_ids})
                    return request.render('game.thanks_page', {})
        else:
            return request.render('game.claim_button_page', {})

    @http.route(['/report/pdf/receipt_download'], type='http', auth='public', methods=['POST'])
    def download_receipt(self, game_id):
        game_data = request.env['game.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        pdf, _ = request.env.ref('game.action_ticket_receipt').sudo()._render_qweb_pdf([int(game_data.id)])
        pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf)),
                          ('Content-Disposition', 'COA; filename="Receipt.pdf"')]
        return request.make_response(pdf, headers=pdfhttpheaders)

    # -----------------Functions of second game-------------

    @http.route('/second-game', type="http", auth="user", website=True)
    def play_second_game(self, **post):
        uid = request.env.user.partner_id
        if uid:
            customer = post.get('customer')
            lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
            if customer:
                customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
                return http.request.render('game.game_two_form', {'partner': customers, 'lottery': lottery})
            else:
                return http.request.render('game.game_two_form', {'partners': uid, 'lottery': lottery})
        else:
            return http.request.render('web.login', )

    @http.route('/open_game', auth='public', type='http', website=True, methods=['POST'])
    def open_second_game(self, input_number, **post):
        partner = request.env.user.partner_id
        lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
        customer = post.get('customers')
        if customer:
            customers = request.env['res.partner'].sudo().search([('id', '=', int(customer))])
            game_wheel = request.env['game.wheel.data'].sudo().create({
                'partner': customers.id if customers else partner.id,
                'create_date': datetime.now(),
                'lottery_wheel': lottery.id,
                'input': input_number,
                'rate': lottery.rate,
                'agent': request.env.user.id,
                'company': lottery.company_id.id,
            })
            return http.request.render('game.game_two', {'game': game_wheel})
        else:
            game_wheel = request.env['game.wheel.data'].sudo().create({
                'partner': partner.id,
                'create_date': datetime.now(),
                'lottery_wheel': lottery.id,
                'input': input_number,
                'rate': lottery.rate,
                'company': lottery.company_id.id,
            })
            return http.request.render('game.game_two', {'game': game_wheel})

    @http.route('/get_result_game_two', auth='public', type='http', website=True, methods=['POST'])
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

    @http.route('/claim_prize_two', type='http', auth="user", methods=['GET'], website=True,
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

    @http.route('/receive_payment_info', type="http", auth="user", website=True,methods=['GET'])
    def receive_payment_info(self, **kwargs):
        abc = len(kwargs)
        print(abc)
        logger.warning("----------------------Request Data ======= %s ====-----------------------", kwargs)
        return str(kwargs)
