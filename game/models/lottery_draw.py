from odoo import fields, models, api, _
import random
from datetime import datetime
from odoo.exceptions import UserError


class LotteryDraw(models.Model):
    _name = "lottery.draw"

    name = fields.Char('Name')
    draw_time = fields.Datetime('Draw Time')
    active_draw = fields.Boolean('Active')
    player_inputs = fields.One2many('game.data', 'draw', string='Players and their lottery numbers')
    first = fields.Integer('First')
    second = fields.Integer('Second')
    third = fields.Integer('Third')
    fourth = fields.Integer('Fourth')
    fifth = fields.Integer('Fifth')
    sixth = fields.Integer('Sixth')
    draw_generated = fields.Boolean('Draw Generated?')

    def generate_numbers(self):
        res = []
        n = 6
        for j in range(n):
            res.append(random.randint(1, 49))
        self.first = res[0]
        self.second = res[1]
        self.third = res[2]
        self.fourth = res[3]
        self.fifth = res[4]
        self.sixth = res[5]
        self.draw_generated = True

    def draw_results(self):
        draws = []
        for item in self:
            draws.append(item.first)
            draws.append(item.second)
            draws.append(item.third)
            draws.append(item.fourth)
            draws.append(item.fifth)
            draws.append(item.sixth)
            for rec in item.player_inputs:
                results = []
                if rec.first in draws:
                    results.append(rec.first)
                if rec.second in draws:
                    results.append(rec.second)
                if rec.third in draws:
                    results.append(rec.third)
                if rec.fourth in draws:
                    results.append(rec.fourth)
                if rec.fifth in draws:
                    results.append(rec.fifth)
                if rec.sixth in draws:
                    results.append(rec.sixth)
                str1 = " "
                list_string = map(str, results)
                rec.draw_result = str1.join(list_string)
                results.clear()
                mail_values = {}
                if rec.partner.name and rec.partner.email:
                    mail_values.update({
                        'body_html': """
                                        <p>Dear """ + rec.partner.name + """</p>
                                    <p>Result of draws has been came out.</p>
                                    <br/>
                                    <br/>
                                    <table class="table table-bordered" style="border: outset;width:27%;">
                            <tr style="height: 70px;border-bottom: 1px solid #ddd;">
                            <td style="height: 70px;border-bottom: 1px solid #ddd;">Your Inputs</td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.first) + """
                                </td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.second) + """
                                </td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.third) + """
                                </td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.fourth) + """
                                </td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.fifth) + """
                                </td>
                                <td style="height: 70px;border-bottom: 1px solid #ddd;">
                                    """ + str(rec.sixth) + """
                                </td>
                            </tr>
                            <tr style="height: 70px; border-bottom: 1px solid #ddd;">
                            <td>Draw Results</td>
                                <td>
                                    """ + str(item.first) + """
                                </td>
                                <td>
                                    """ + str(item.second) + """
                                </td>
                                <td>
                                    """ + str(item.third) + """
                                </td>
                                <td>
                                    """ + str(item.fourth) + """
                                </td>
                                <td>
                                    """ + str(item.fifth) + """
                                </td>
                                <td>
                                    """ + str(item.sixth) + """
                                </td>
                            </tr>
                        </table>
                        <br/>
                        <br/>
                        Matched numbers are : """ + str1.join(list_string) + """
                        
                                                        """
                    })
                    mail_values.update({
                        'subject': rec.partner.name + '- Draw Result',
                        'email_to': rec.partner.email,
                    })
                    msg_id_managaer = self.env['mail.mail'].create(mail_values)
                    msg_id_managaer.send()
