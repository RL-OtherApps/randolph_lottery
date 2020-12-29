# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
import logging
from datetime import datetime,date

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
            return http.request.render('game.game_two_form', {})
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

    @http.route('/open_game', auth='public', type='http', website=True, methods=['POST'])
    def open_first_game(self, input_number):
        partner = request.env.user.partner_id
        lottery = request.env['lottery.wheel'].sudo().search([('active_lottery', '=', True)], limit=1)
        game_wheel = request.env['game.wheel.data'].sudo().create({
            'partner': partner.id,
            'create_date': datetime.now(),
            'lottery_wheel': lottery.id,
            'input': input_number,
            'rate': lottery.rate,
        })
        return http.request.render('game.game_two', {'game': game_wheel})

    @http.route('/get_result_game_two', auth='public', type='http', website=True, methods=['POST'])
    def save_result_game_two(self, result_number, game_id):
        game_data = request.env['game.wheel.data'].sudo().search([('id', '=', int(game_id))], limit=1)
        if int(game_data.input) == int(result_number):
            amount = int(result_number) * int(game_data.rate)
            game_data.update({'result': result_number, 'amount_won': amount})
            return http.request.render('game.game_two_form', {})
        else:
            game_data.update({'result': result_number, 'amount_won': 0})
            return http.request.render('game.game_two_form', {})

    @http.route('/claim_prize/<string:id>', type='http', auth="user", methods=['GET'], website=True,
                csrf=False)
    def contract_details(self, id, **post):
        game_data = request.env['game.data'].sudo().search([('id', '=', int(id))], limit=1)
        partner = request.env.user.partner_id
        name = post.get('name')
        acc_number = post.get('acc_number')
        ifsc = post.get('ifsc')
        values={'game_data':game_data}
        if name and acc_number and ifsc:
            partner.update({
                'full_name': name,
                'acc_number': acc_number,
                'ifsc': ifsc,
            })
            product_id = request.env['product.product'].sudo().search([('name', '=', 'Lottery Draw Winner')])
            journal = request.env['account.journal'].sudo().search([('name', '=', 'Vendor Bills')],limit=1)
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
        return request.render('game.claim_button_page', {})
