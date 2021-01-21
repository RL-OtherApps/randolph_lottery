from odoo import fields, models, api, _
import random
import collections
from datetime import datetime
from odoo.exceptions import UserError


class BoletLotteryDraw(models.Model):
    _name = "bolet.lottery.draw"

    name = fields.Char('Name')
    draw_time = fields.Datetime('Draw Time')
    active_draw = fields.Boolean('Active')
    player_inputs = fields.One2many('bolet.game.data', 'draw', string='Players and their lottery numbers')
    first = fields.Integer('First')
    second = fields.Integer('Second')
    third = fields.Integer('Third')
    draw_generated = fields.Boolean('Draw Generated?')
    first_prize = fields.Integer('If 1st digit matched')
    second_prize = fields.Integer('If 2nd digit matched')
    third_prize = fields.Integer('If 3rd digit matched')
    rate = fields.Char('Rate')
    company_id = fields.Many2one('res.company', 'company', default=lambda self: self.env.company.id)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    game_id = fields.Integer('Game ID')

    def generate_numbers(self):
        res = []
        n = 6
        for j in range(n):
            res.append(random.randint(1, 49))
        self.first = res[0]
        self.second = res[1]
        self.third = res[2]
        self.draw_generated = True

    def draw_results(self):
        draws = []
        draws.extend([self.first, self.second, self.third])
        for rec in self.player_inputs:
            inputs = []
            if rec.first:
                inputs.append(rec.first)
            if draws[0] == inputs[0]:
                rec.winning = "1st Digit Matched"
                rec.winning_amount = self.first_prize * int(rec.betting_amount)
            elif draws[1] == inputs[0]:
                rec.winning = "2nd Digit Matched"
                rec.winning_amount = self.second_prize * int(rec.betting_amount)
            elif draws[2] == inputs[0]:
                rec.winning = "3rd Digit Matched"
                rec.winning_amount = self.third_prize * int(rec.betting_amount)
            else:
                rec.winning = "None"
                rec.winning_amount = 0
            inputs.clear()
            mail_values = {}

            if rec.partner.name and rec.partner.email:
                url = self.get_base_url() + '/claim_prize/' + str(rec.id)
                if int(rec.winning_amount) > 0:
                    mail_values.update({
                        'body_html': """
                        <p>Dear """ + rec.partner.name + """</p>
                        <p>Result of draws has been came out.</p>
                        <br/>
                        <br/>
                        <table class="table table-bordered" style="width:27%;border-collapse: collapse;border-style:double;text-align:center;">
                        <tr>
                        <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Your Input</td>
                        <td colspan="3" style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Results</td>
                        </tr>
                        <tr style="height: 70px;border-bottom: 1px solid #101820FF;">
                        <td style="background-color:#F2AA4CFF;color:#101820FF;">
                            """ + str(rec.first) + """
                        </td>
                        <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                            """ + str(self.first) + """
                        </td>
                        <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                            """ + str(self.second) + """
                        </td>
                        <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                            """ + str(self.third) + """
                        </td>
                        </tr>
                    </table>
                    <br/>
                    <br/>
                    You have won : """ + rec.winning + """<br/>
                    Winning Amount : """ + rec.winning_amount + """
                    <br/>
                    <button style="background-color:#875A7B;color:white; padding:5px; font-size:16px;">
                            <a style="color:white; text-decoration:none;" href='""" + url + """'> Claim Prize </a></button>
                    <br/>
                                                    """
                    })
                else:
                    mail_values.update({
                        'body_html': """
                                                <p>Dear """ + rec.partner.name + """</p>
                                                <p>Result of draws has been came out.</p>
                                                <br/>
                                                <br/>
                                                <table class="table table-bordered" style="width:27%;border-collapse: collapse;border-style:double;text-align:center;">
                                                <tr>
                                                <td  style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Your Input</td>
                                                <td colspan="3" style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Results</td>
                                                </tr>
                                                <tr style="height: 70px;border-bottom: 1px solid #101820FF;">
                                                <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                    """ + str(rec.first) + """
                                                </td>
                                                <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                    """ + str(self.first) + """
                                                </td>
                                                <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                    """ + str(self.second) + """
                                                </td>
                                                <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                    """ + str(self.third) + """
                                                </td>
                                                </tr>

                                            </table>
                                            <br/>

                                            <br/>
                                            You have won : """ + rec.winning + """<br/>
                                            Winning Amount : """ + rec.winning_amount + """

                                            <br/>
                                                                            """
                    })
                mail_values.update({
                    'subject': rec.partner.name + '- Bolet Draw Result',
                    'email_to': rec.partner.email,
                })
                msg_id_managaer = self.env['mail.mail'].create(mail_values)
                msg_id_managaer.send()


class BoletGameData(models.Model):
    _name = "bolet.game.data"

    partner = fields.Many2one('res.partner', 'Customer')
    agent = fields.Many2one('res.users', 'Agent')
    company = fields.Many2one('res.company', 'Company')
    draw = fields.Many2one('bolet.lottery.draw', 'Draw')
    first = fields.Integer('First')
    create_date = fields.Datetime('Date')
    ticket_number = fields.Char('Ticket Number')
    draw_result = fields.Char('Draw Results')
    winning = fields.Char('Winning')
    winning_amount = fields.Char('Winning Amount')
    sale_order = fields.Many2one('sale.order', 'Sale Order')
    transaction_id = fields.Char('Transaction ID')
    betting_amount = fields.Char('Betting AMount')
