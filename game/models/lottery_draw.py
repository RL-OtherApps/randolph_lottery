from odoo import fields, models, api, _
import random
import collections
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
    first_prize = fields.Integer('First Digit', currency_field='currency_id')
    second_prize = fields.Integer('Front Pair', currency_field='currency_id')
    third_prize = fields.Integer('Back Pair', currency_field='currency_id')
    fourth_prize = fields.Integer('First Three', currency_field='currency_id')
    fifth_prize = fields.Integer('Back Three', currency_field='currency_id')
    sixth_prize = fields.Integer('Take it all', currency_field='currency_id')
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
        self.fourth = res[3]
        self.fifth = res[4]
        self.sixth = res[5]
        self.draw_generated = True

    def draw_results(self):
        draws = []
        for item in self:
            draws.extend([item.first, item.second, item.third, item.fourth, item.fifth, item.sixth])
            for rec in item.player_inputs:
                results = []
                inputs = []
                inputs.extend([rec.first, rec.second, rec.third, rec.fourth, rec.fifth, rec.sixth])
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
                if collections.Counter(draws) == collections.Counter(inputs):
                    rec.winning = "All"
                    rec.winning_amount = item.sixth_prize
                else:
                    if draws[0] == inputs[0]:
                        temp1 = []
                        temp2 = []
                        temp1.extend([draws[0], draws[1], draws[2]])
                        temp2.extend([inputs[0], inputs[1], inputs[2]])
                        temp11 = []
                        temp12 = []
                        temp11.extend([draws[0], draws[1]])
                        temp12.extend([inputs[0], inputs[1]])
                        if collections.Counter(temp1) == collections.Counter(temp2):
                            rec.winning = "First Three"
                            rec.winning_amount = item.third_prize
                        elif collections.Counter(temp11) == collections.Counter(temp12):
                            rec.winning = "First Pair"
                            rec.winning_amount = item.second_prize
                        else:
                            rec.winning = "First digit"
                            rec.winning_amount = item.first_prize
                    else:
                        temp1 = []
                        temp2 = []
                        temp1.extend([draws[3], draws[4], draws[5]])
                        temp2.extend([inputs[3], inputs[4], inputs[5]])
                        temp11 = []
                        temp12 = []
                        temp11.extend([draws[4], draws[5]])
                        temp12.extend([inputs[4], inputs[5]])
                        if collections.Counter(temp1) == collections.Counter(temp2):
                            rec.winning = "Back Three"
                            rec.winning_amount = item.sixth_prize
                        elif collections.Counter(temp11) == collections.Counter(temp12):
                            rec.winning = "Back Pair"
                            rec.winning_amount = item.fifth_prize
                        else:
                            rec.winning = "None"
                            rec.winning_amount = 0
                results.clear()
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
                            <tr style="height: 70px;border-bottom: 1px solid #101820FF;">
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Your Inputs</td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.first) + """
                            </td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.second) + """
                            </td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.third) + """
                            </td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.fourth) + """
                            </td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.fifth) + """
                            </td>
                            <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                """ + str(rec.sixth) + """
                            </td>
                            </tr>
                            <tr style="height: 70px; border-bottom: 1px solid #ddd;">
                            <td style="background-color:#F2AA4CFF;color:#101820FF;">Draw Results</td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                """ + str(item.first) + """
                            </td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                """ + str(item.second) + """
                            </td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                """ + str(item.third) + """
                            </td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                """ + str(item.fourth) + """
                            </td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                """ + str(item.fifth) + """
                            </td>
                            <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                """ + str(item.sixth) + """
                            </td>
                            </tr>
                        </table>
                        <br/>
                        
                        <br/>
                        Matched numbers are : """ + str1.join(list_string) + """<br/>
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
                                                    <tr style="height: 70px;border-bottom: 1px solid #101820FF;">
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">Your Inputs</td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.first) + """
                                                    </td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.second) + """
                                                    </td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.third) + """
                                                    </td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.fourth) + """
                                                    </td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.fifth) + """
                                                    </td>
                                                    <td style="height: 70px;border-bottom: 1px solid #ddd;background-color:#101820FF;color:#F2AA4CFF;">
                                                        """ + str(rec.sixth) + """
                                                    </td>
                                                    </tr>
                                                    <tr style="height: 70px; border-bottom: 1px solid #ddd;">
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;">Draw Results</td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                        """ + str(item.first) + """
                                                    </td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                        """ + str(item.second) + """
                                                    </td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;">
                                                        """ + str(item.third) + """
                                                    </td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                                        """ + str(item.fourth) + """
                                                    </td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                                        """ + str(item.fifth) + """
                                                    </td>
                                                    <td style="background-color:#F2AA4CFF;color:#101820FF;border-color:#F2AA4CFF;">
                                                        """ + str(item.sixth) + """
                                                    </td>
                                                    </tr>
                                                </table>
                                                <br/>

                                                <br/>
                                                Matched numbers are : """ + str1.join(list_string) + """<br/>
                                                You have won : """ + rec.winning + """<br/>
                                                Winning Amount : """ + rec.winning_amount + """
                                        
                                                <br/>
                                                                                """
                        })
                    mail_values.update({
                        'subject': rec.partner.name + '- Draw Result',
                        'email_to': rec.partner.email,
                    })
                    msg_id_managaer = self.env['mail.mail'].create(mail_values)
                    msg_id_managaer.send()
